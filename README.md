# KOSMOS — your virtual makeup bag

## Index
- <a href="#preface">Preface</a>
- <a href="#pre-requisites">Pre-requisites</a>
- <a href="#mission">Mission</a>
- <a href="#how-kosmos-is-different-from-other-cs50w-projects">How KOSMOS is Different From Other CS50W Projects</a>
- <a href="#current-features">Current Features</a>
- <a href="#future-features">Future Features</a>

## Preface
This project was created as my capstone project for CS50's Web Programming with Python and JavaScript course. It uses Python Django on the back-end, and vanilla JavaScript on the front-end.

## Pre-requisites
To run, please download the files in the requirements.txt file. Recommended browser: Google Chrome.
To run the email and notification functionality, you'll need to run the Celery task queue, and also change the EMAIL_HOST, EMAIL_HOST_USER, and EMAIL_HOST_PASSWORD to the SMTP server, email, and email password of your choice. 

## Mission
<p>KOSMOS was designed to rid people of the burden of makeup expiry dates. It allows registered users to add products to their "virtual makeup bags," and input the expiry dates for these products. Upon expiry, the user will be notified via the site and email, reminding users to throw away those icky products and/or replace them. </p>
<p>Beyond the virtual makeup bags, KOSMOS allows users to curate "collections" of makeup products and even publish them for other KOSMOS users to see and "heart." While viewing makeup products from our database of over 900, users can read and write reviews for products. KOSMOS being a third-party website eliminates any bias or paid-for commentary of these products.</p>
<p>Overall, the main goal of KOSMOS is to make the makeup buying and maintaining process simple and transparent. We're here to make making you beautiful beautiful in itself.</p>

## How KOSMOS is Different From Other CS50W Projects
<p>KOSMOS is NOT an ecommerce website. There is no ordering or buying in place. When adding to makeup bags, it is assumed the user already owns these products. KOSMOS is a way to digitize one's physical collection of makeup products. The makeup bags not only digitize one's physical collection, but also let KOSMOS know which products one would like to be notified about. KOSMOS collections, on the other hand, provide users a way to curate lists of makeup products, perhaps for certain situations. KOSMOS collections are the only way users can directly interact with one another.</p>

<p>KOSMOS uses Python (Django), HTML, CSS/SASS, and JavaScript. JavaScript is used to dynamically create elements and carry out events, such as automatically calculating expiry dates based on the user's chosen opening date, editing collection and makeup bag details, heart functionality, etc. It communicates with the Django-powered server using Fetch API. KOSMOS' database was imported from the <a href="makeup-api.herokuapp.com">Makeup API</a>, with modifications carried out by me, and average rating calculated by user reviews.</p>

<p>I believe my project is sufficiently distinct from past CS50W projects and much more complex. I definitely had the most trouble with the email functionality, as it was difficult to sync the Django server with the Google SMTP server, the Celery task queue, and the RabbitMQ message broker software. I hope this project satisfies whoever is marking this, it's been a pleasure taking the course!</p>

## Current Features
- Mobile responsive!
<br>![gif showing KOSMOS site responsive design](https://github.com/me50/isabellaenriquez/blob/web50/projects/2020/x/capstone/capstone/kosmos/static/kosmos/images/responsiveness.gif)
<br>File explanation, along with their respective views.py functions, if applicable:
- Navigation bar (created in layout.html)
- Home page (index.html, views.index): The home page, with sections for KOSMOS' story, and the founder's story
- My Makeup Bag (bag.html, bag.js, views.my_bag): Users can add and remove products to their digital makeup bags. For each products, the user can add notes, an opening date, an expiry date, and enable notifications. If notifications are enabled, users will receive a notification on the site and via email when the respective product is expired.
- Registration/Login/Logout (register.html, views.register, login.html, views.login_view, logout_view): KOSMOS has a registration system which allows users to create free accounts, and log back into them any time.
- My Profile (profile.html, views.profile): Registered users can view their profiles, which includes their profile statistics as well as their five most recently published collections.
- product_layout.html gives all pages displaying products a grid layout
- Browse Products (products.html, views.products): Users can browse a database of over 900 products. Users can additionally sort the products and filter to narrow down products shown. Pagination is used.
- Search (search.html, views.search): Users can search the database of makeup products.
- View Product (view_product.html, view_product.js, views.view_product): Users can view product information, including brand, price, average rating, available colours, types, categories, and tags. Registered users can review the product, if they haven't already, and add the product to their makeup bag and/or existing collections. 
- My Collections (collections.html, views.my_collections): Registered users can view a list of their respective collections, both public and private.
- Public Collections (collections.html, views.public_collections): Users, logged in or not, can view a list of published collections.
- Curate (curate.html, views.curate): Registered users can create collections, choosing a title, description (optional), banner, and whether or not they would like that collection to be public.
- View Collection (view_collection.html, view_collection.js, views.view_collection): Users can browse a collection's content. If the user is author, they can make changes to the collection's details.
- Mailbox (mailbox.html, mailbox.js, views.mailbox): This is where registered users receive notifications for product expiries. An exclamation mark will appear beside the mailbox when the user has any outstanding notifications. Notifications are removed when the user removes the associated product or extends the expiry date. 
- Emails (email.html): This is the template for the emails sent out to users when an expired product is detected. The actual functionality is carried out by Celery, living in celery.py and tasks.py. Assuming the servers are all up and running, expiry detection takes place at the start of every day (GMT-4). When a product is detected, the database is changed and an email is sent out to the respective user by RabbitMQ via Google SMTP.

### Management Commands
These commands were made to modify my large database, as doing it manually would've taken far too long.
- check_images : Goes through database and checks to see if images are valid. If not, remove the image link.
- import : Imported the database, with each entry as a MakeupProduct, with code to make sure the information fit the formats created in models.py.
- lip_fix : I noticed there was a lack of consistency with some of the lip products in the database (for example, the original database had lipstick as both a product type and category, with lip gloss and liner falling under the lipstick category). I decided to make it so there was an umbrella "lip product" product type, with lip stick, lip liner, lip gloss, and lip stain all falling as categories under it.

### Watch the demo!
Click <a href="https://www.youtube.com/watch?v=4kyZ7RuZS3k&feature=youtu.be">here.</a>

## Future Features
- Improved Filters: users can browse makeup by colour groups; filters can be applied to searches
- Improved Search: search not only through products, but for users, collections, etc.
- Custom Makeup Products: enable users to create custom makeup products to make up for those that aren't currently in the database
- Makeup Hacks: users can post makeup "hacks" for other users to read and even heart
- Private Collection Sharing: users can authorize others to view their private collections without making the collection public 
- Currency Conversion: users can browse products in their chosen currency
- Following: users can follow other users; a "Following" feed is created full of the collections of the people the user follows
- Profile Customization: users can set an avatar for themselves, a short biography, connect their other social media, and customize the look of their profiles and makeup bags with themes