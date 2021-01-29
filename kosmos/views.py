from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *
from django.db import IntegrityError
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.urls import reverse
import json

def index(request):
    return render(request, 'kosmos/index.html')

def register(request):
    if request.user.is_authenticated: # redirect if user already logged in
        return HttpResponseRedirect(reverse("index"))
    if request.method == "POST": # register request mad
        username = request.POST["username"]
        email = request.POST["email"]

        # confirm password
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.error(request, "Passwords must match.")
            return render(request, "kosmos/register.html", context={
                "page_title": "new user"
            })
        
        # try to create new user
        try: 
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError: # user already exists
            messages.error(request, "Sorry, that username has already been taken!")
            return render(request, "kosmos/register.html", context={
                "page_title": "new user"
            })
        login(request, user) # successful account creation
        return HttpResponseRedirect(reverse('index'))
    
    else: 
        return render(request, "kosmos/register.html", context={
                "page_title": "new user",
            })

def login_view(request):
    if request.user.is_authenticated: # redirect if user already logged in
        return HttpResponseRedirect(reverse("index"))
    if request.method == "POST":

        # try to login
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # check if successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Sorry, the username and/or password was invalid.")
            return render(request, "kosmos/login.html", context={
                "page_title": "returning user"
            })
    else:
        return render(request, "kosmos/login.html", context={
            "page_title": "returning user"
        })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index')) # redirect to home page

def products(request):
    # TODO: reset button for filters
    # user wants it ordered by certain category
    ordered_by = request.GET.get('orderBy')
    type_filter = request.GET.get('typeRadios')
    if not type_filter:
        type_filter = 'all'
    cat_filter = request.GET.get('catRadios')
    if not cat_filter:
        cat_filter = 'all'

    if type_filter == 'all': # no type filter
        if cat_filter =='all': # no category filter
            all_products = MakeupProduct.objects.all()
        else: # no type filter, yes category filter
            all_products = MakeupProduct.objects.filter(category=cat_filter)
    elif cat_filter == 'all': # no category filter, yes type filter
        all_products = MakeupProduct.objects.filter(product_type=type_filter)
    else: # yes type filter, yes category filter
        all_products = MakeupProduct.objects.filter(product_type=type_filter, category=cat_filter)

    if not ordered_by:
        ordered_by = 'name'
    #all_products = MakeupProduct.objects.all().order_by(ordered_by)
    if ordered_by == 'name': 
        # sort by name, ignoring whitespace and caps
        all_products = sorted(all_products, key=lambda product: ''.join(product.name.lower().split()))
    else:
        if ordered_by[0] == "-":
            all_products = sorted(all_products, reverse=True, key=lambda product: product.__dict__[ordered_by[1:]])
        else:
            all_products = sorted(all_products, key=lambda product: product.__dict__[ordered_by])

    paginated_products = paginate(request, all_products)
    
    current_page = paginated_products.number
    last_page = len(paginated_products.paginator.page_range)
    if current_page >= 3:
        start_range = current_page - 3
    else:
        start_range = 0
    if current_page <= (last_page - 3):
        end_range = current_page + 3
    else:
        end_range = last_page
    page_num_range = list(paginated_products.paginator.page_range)[start_range:end_range]

    return render(request, 'kosmos/products.html', context={
        'page_title': 'browse products',
        'products': paginated_products,
        'ordered_by': ordered_by,
        'product_type': type_filter,
        'cat': cat_filter,
        'page_num_range': page_num_range,
        'last_page': last_page,
        'product_types': MakeupProduct.PRODUCT_TYPES,
        'categories': MakeupProduct.CATEGORIES
    })

def paginate(request, items):
    page = request.GET.get('page', 1)
    paginator = Paginator(items, 20)
    try:
        paginated_items = paginator.page(page)
    except PageNotAnInteger:
        paginated_items = paginator.page(1)
    except EmptyPage:
        paginated_items = paginator.page(paginator.num_pages)
    return paginated_items

def view_product(request, product_id):
    product = MakeupProduct.objects.get(id=product_id)
    in_bag = False
    reviewed = False
    user = request.user
    if user.is_authenticated: 
        try:
            bag_item = MakeupBagItem.objects.filter(product=product, bag=user.bag)
            if len(bag_item) > 0:
                in_bag = True
        except:
            pass
    reviews = Review.objects.filter(product=product).order_by('-timestamp')
    for review in reviews:
        if review.author == user:
            reviewed = True
    if request.method == "POST": # add object to bag/collection
        add_to = request.POST["selection"]
        if add_to == 'bag': # add to bag
            try:
                bag = request.user.bag
            except: # if makeup bag hasn't been created yet
                bag = MakeupBag.objects.create(owner=request.user)
                bag.save()

            open_date = request.POST["openDate"]
            print("open:" + open_date + '.')
            expiry = request.POST["expiry"]
            send_notifs = False
            if 'notify' in request.POST: # send notifications when product is expired
                send_notifs = True
            """ testing
            testItem = {
                'product': product,
                'bag': bag,
                'open': open_date,
                'expiry': expiry,
                'notifs': send_notifs
            }
            print(testItem)
            return HttpResponseRedirect(reverse('view_product', args=(product_id,)))"""
        
            item = MakeupBagItem.objects.create(bag=bag, product=product, notifications=send_notifs)
            if open_date is not None and open_date != '':
                item.open_date = open_date
                print("saved", item.open_date)
            if expiry is not None and expiry!= '':
                item.expiry = expiry
            if len(request.POST['notes']) >0:
                item.notes = request.POST['notes']
            item.save()
            messages.success(request, 'The product was added successfully!')
        else: # add to collection
            c = Collection.objects.get(id=add_to)
            item = CollectionItem.objects.create(product=product, collection=c)
            item.save()
            c.save() # save to update timestamps
            messages.success(request, 'The product was added to your collection successfully!')
        
        return HttpResponseRedirect(reverse('view_product', args=(product_id,)))
    else:
        tags = list(product.tags.all())
        readable_tags = []
        for tag in tags:
            readable_tags.append(tag.get_name_display())
        colours = list(product.colours.all())
        if request.user.is_authenticated:
            collections = list(request.user.collections.all())
        else:
            collections = []
        print(collections)
        return render(request, 'kosmos/view_product.html', context={
            'page_title': product.name,
            'product': product,
            'tags': readable_tags,
            'collections': collections,
            "in_bag": in_bag,
            "reviewed": reviewed,
            "reviews": reviews,
            "colours": colours
        })

def search(request):
    query = request.GET.get('q')
    product_query = query.replace(' ', '_') # replace spaces for underscores
    product_query = product_query.replace('/', '_')
    product_query = product_query.lower()
    product_types = dict(MakeupProduct.PRODUCT_TYPES)
    categories = dict(MakeupProduct.CATEGORIES)

    if product_query in product_types:
        results = MakeupProduct.objects.filter(product_type__iexact=product_query)
    elif product_query in categories:
        results = MakeupProduct.objects.filter(category__iexact=product_query)
    else:
        results = MakeupProduct.objects.filter(Q(brand__icontains=query) | Q(name__icontains=query))
    
    paginated_results = paginate(request, results)
    current_page = paginated_results.number
    last_page = len(paginated_results.paginator.page_range)
    if current_page > 5:
        start_range = current_page - 6
    else:
        start_range = 0
    if current_page <= (last_page - 5):
        end_range = current_page + 5
    else:
        end_range = last_page
    page_num_range = list(paginated_results.paginator.page_range)[start_range:end_range]

    return render(request, 'kosmos/search.html', context={
        'page_title': 'Search results for \"' + query + '\"',
        'products': paginated_results,
        'page_num_range': page_num_range,
        'last_page': last_page,
        'query': query
    })

@login_required
def my_bag(request):
    if (request.method == 'PUT'):
        put_data = json.loads(request.body)
        handle_put(request, put_data)
    user = request.user
    # TODO: paginate
    try:
        bag = MakeupBag.objects.get(owner=user)
    except: # bag hasn't been created yet
        bag = MakeupBag.objects.create(owner=user)
    
    bag_items = MakeupBagItem.objects.filter(bag=bag).order_by('-open_date')
    return render(request, 'kosmos/bag.html', context={
        'page_title': 'my makeup bag',
        'bag': bag,
        'items': bag_items
    })

@login_required
def my_collections(request):
    user = request.user
    collections = Collection.objects.filter(author=user).order_by('-timestamp')

    return render(request, 'kosmos/collections.html', context={
        'page_title': 'my collections',
        'collections': collections
    })

def public_collections(request):
    collections = Collection.objects.filter(public=True).order_by('-timestamp')
    return render(request, 'kosmos/collections.html', context={
        'page_title': 'public collections',
        'collections': collections
    })

@login_required
def curate(request):
    if request.method == "POST":
        author = request.user
        public = False
        if 'public' in request.POST:
            public = True
        title = request.POST['title']
        dscrpt = request.POST['dscrpt']
        banner = request.POST['banner']
        c = Collection.objects.create(author=author, public=public, title=title, description=dscrpt, banner_num=banner)
        c.save()
        # redirect to collection page
        return HttpResponseRedirect(reverse('view_collection', args=(c.id,)))
    else:
        return render(request, 'kosmos/curate.html', context={
            'page_title': 'new collection'
        })

def view_collection(request, collect_id):
    # TODO: check if owner is the one making the requests
    try:
        c = Collection.objects.get(id=collect_id)
        items = c.items.all()
        hearts = c.hearts.count()
    except: # requested an invalid collection id
        messages.error(request, 'That collection does not exist.')
        return HttpResponseRedirect(reverse('index'))

    user = request.user
    liked = False
    if user.is_authenticated:
        try:
            if CollectionHeart.objects.get(user=user, collection=c): # user has liked the collection
                liked = True
        except:
            pass

    if c.author !=user: # current user is not the author
        if request.method !="GET":
            if request.method == "PUT" and user.is_authenticated: # only logged in users can heart
                put_data = json.loads(request.body)
                if put_data['type'] == 'heart' or put_data['type'] == 'unheart':
                    handle_put(request, put_data)
                else:
                    messages.error(request, 'You do not have permissions to alter this collection.')
            else:
                messages.error(request, 'You do not have permissions to alter this collection.')
        if not c.public: # collection is private
            messages.error(request, 'You are not authorized to view the requested collection.')
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'kosmos/view_collection.html', context={
                'page_title': c.__str__,
                'collection': c,
                'items': items,
                'hearts': hearts,
                'user': user,
                'liked': liked
            })
    else: # collection is owned by current user
        if (request.method == 'PUT'):
            put_data = json.loads(request.body)
            handle_put(request, put_data)
        if(request.method == 'DELETE'):
            data = json.loads(request.body)
            c.delete()
        else:
            return render(request, 'kosmos/view_collection.html', context={
                    'page_title': c.__str__,
                    'collection': c,
                    'items': items,
                    'edit': True,
                    'hearts': hearts,
                    'user': user,
                    'liked': liked
                })

def handle_put(request, data):
    if (data['type'] == 'remove_item'): # delete entry in collection
        item_id = data['delete_id']
        del_from = data['from']
        if del_from == 'bag':
            item = MakeupBagItem.objects.get(id=item_id)
        elif del_from == 'collection':
            item = CollectionItem.objects.get(id=item_id)
            c = Collection.objects.get(id=data['collection'])
            c.save() # for timestamp
        item.delete()
        if 'notif' in data:
            # remove from notifications
            u = request.user
            if MakeupBagItem.objects.filter(bag=u.bag, is_expired=True).count() <= 0: # zero expired products in bag
                u.has_notifications = False
                u.save()
                
    elif (data['type'] == 'edit_collection'): # edit collection details
        c_id = data['collection']
        c = Collection.objects.get(id=c_id)
        c.title = data['title']
        c.public = data['notify']
        c.description = data['dscrpt']
        c.save()
    elif (data['type'] == 'heart'): # heart collection
        c_id = data['collection']
        c = Collection.objects.get(id=c_id)
        u = request.user
        h = CollectionHeart.objects.create(user=u, collection=c)
        h.save()
    elif (data['type'] == 'unheart'): # unheart collection
        c_id = data['collection']
        c = Collection.objects.get(id=c_id)
        u = request.user
        h = CollectionHeart.objects.get(user=u, collection=c)
        h.delete()
    elif (data['type'] == 'edit_bag_item'): # edit items in makeup bag
        i_id = data['item']
        i = MakeupBagItem.objects.get(id=i_id)
        if request.user.bag != i.bag or request.user.bag is None: # user is not authorized
            messages.error('You are not authorized to alter this makeup bag.')
            return HttpResponseRedirect(reverse('index'))
        i.open_date = data['open']
        if str(data['expiry']) > str(i.expiry) and i.expiry == datetime.date.today(): # user changed expiry to later date
            i.is_expired = False
            print('no longer expired')
            
        i.expiry = data['expiry']
        i.notifications = data['notify']
        i.notes = data['notes']
        i.save()
        if (count_notifications(request) == 0):
            u = request.user
            u.has_notifications = False
            u.save()
    
@login_required
def review(request):
    if request.method == "POST":
        product_id = request.POST['product']
        p = MakeupProduct.objects.get(id=product_id)
        author = request.user
        content = request.POST['text']
        rating = request.POST['stars']
        r = Review.objects.create(product=p, author=author, content=content, stars=rating)
        r.save()
        p.avg_rating = ((p.avg_rating * (p.reviews.count() -1)) + int(r.stars))/(p.reviews.count())
        p.save()
        messages.success(request, 'Your review for ' + str(p) + ' has been posted!')
        return HttpResponseRedirect(reverse('view_product', args=(product_id,)))
    else:
        messages.error('Invalid request.')
        return HttpResponseRedirect(reverse('index'))

@login_required # only KOSMOS users can view profiles
def profile(request, username):
    try:
        user = User.objects.get(username=username)
        # is_logged_in = (user==request.user) uncomment for future profile customization options
    except:
        messages.error(request, "The requested user does not exist.")
        return HttpResponseRedirect(reverse('index'))

    reviews = Review.objects.filter(author=user).order_by('-timestamp')
    avg_rating = 0
    review_count = len(reviews)
    if review_count > 0:
        for review in reviews:
            avg_rating += review.stars
        avg_rating /= review_count

    # only retrieve public collections
    collections = Collection.objects.filter(author=user, public=True).order_by('-timestamp')
    hearts = 0
    for collection in collections:
        hearts+= len(collection.hearts.all())
    print('here3')
    return render(request, 'kosmos/profile.html', context={
        'user': user,
        'page_title': '@' + user.username + '\'s profile',
        'review_count': review_count,
        'avg_rating': avg_rating,
        'collections': collections,
        'collection_count': len(collections),
        'hearts': hearts
        # 'is_logged_in': is_logged_in 
    })

@login_required
def mailbox(request):
    if request.method == 'PUT':
        put_data = json.loads(request.body)
        handle_put(request, put_data)
    user = request.user
    try:
        expired_items = MakeupBagItem.objects.filter(is_expired=True, bag=user.bag).order_by('-expiry')
    except:
        expired_items = []
        
    return render(request, 'kosmos/mailbox.html', context={
        'page_title': 'my mailbox',
        'user': user,
        'expired_items': expired_items,
        'notification_count': expired_items.count()
    })

def count_notifications(request):
    try:
        user = request.user
        expired_items = MakeupBagItem.objects.filter(is_expired=True, bag=user.bag)
        count = expired_items.count()
    except:
        count = 0
        
    return count