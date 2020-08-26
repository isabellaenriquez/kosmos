# for celery stuff
# need to do broker stuff befoe continuing this stuff:https://www.youtube.com/watch?v=b-6mEAr1m-A

from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from celery.task import periodic_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import User, MakeupBagItem
import datetime

#@periodic_task(run_every=crontab(hour=17, minute=50))
def test():
    print('success?')

#@periodic_task(run_every=crontab(hour=18, minute=25))
def test_html_email():
    print('testing')
    html_msg = render_to_string('kosmos/email.html', {'user': 'cs50-bot', 'product': 'lipstick', 'notes': ''})
    send_mail(
        'Your lipstick is expired!',
        'The lipstick by KOSMOS has expired. Replace it or edit expiry on KOSMOS.',
        'KOSMOS — your virtual makeup bag <noreplykosmos@gmail.com>',
        ['hisefox287@corsj.net'],
        fail_silently=False,
        html_message=html_msg
    )
    print('sent!')

@periodic_task(run_every=crontab(hour=5, minute=0))
def check_expiries():
    print('checking expiries')
    today = datetime.date.today() 
    expired_products = MakeupBagItem.objects.filter(expiry=today, notifications=True)
    for product in expired_products:
        if not product.is_expired:
            product.is_expired = True
            product.save()
        print('expired product detected!')
        user = product.bag.owner
        if not user.has_notifications:
            user.has_notifications = True
            user.save()
        html_msg = render_to_string('kosmos/email.html', {'user': user, 'product': product.product.name, 'notes': product.notes, 'item_img': product.product.img })
        send_mail(
            'Your ' + product.product.name + ' is expired!',
            'The ' + product.product.name + ' by ' + product.product.brand + ' has expired. Replace it or edit expiry on KOSMOS.',
            'KOSMOS — your virtual makeup bag <noreplykosmos@gmail.com>',
            [user.email],
            fail_silently=False,
            html_message=html_msg
        )

