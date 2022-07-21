from requests import request
from House.models import *
from House.forms import ApartmentLevel
from django import template
from django.shortcuts import render
import datetime
from House.models import AdminMessage, DevelopmentMessage
from House.views import subscriber
from customer.models import MailMessage, Subscribers
from payment.models import BookItem, Payment

register = template.Library()


@register.simple_tag(name='my_apartment')
def my_contacts():
    apartments = Apartment.objects.all().last()
    room = Room.objects.filter(flat_id_rooms=apartments.flat_id)
    
    return room

@register.filter(expects_localtime=True)
def is_old_date(value):
    if isinstance(value, datetime.datetime):
        value = value.date()
    delta = value - datetime.date.today()
    return delta.days >= 0


@register.simple_tag(name='my_messages')
def all_messages():
    admin = AdminMessage.objects.count()
    dev = DevelopmentMessage.objects.count()
    

    user = User.objects.all()
    subscribers = Subscribers.objects.all()        
    for user in user:
        for subscriber in subscribers:
            if user.email == subscriber.email:
                mail = MailMessage.objects.count()
            else:
                mail = MailMessage.objects.count()
    
    all = int(admin) + int(dev) + int(mail)
    return all


@register.simple_tag(name='my_payment')
def second_messages():
    admin = Payment.objects.count()
    return admin


@register.simple_tag(name='low_price')
def lowest_price():
    new_room = []
    estate = Estate.objects.all()
    admin = Room.objects.all()
    for estate in estate:
        for rooms in admin:
            if rooms.apartment_name_rooms == estate.estate_name:
                new_room.append(rooms.price)
    return admin
    



# @register.filter(expects_localtime=True)
# def is_old_date(value):
#     if isinstance(value, datetime.datetime):
#         value = value.date()
#     delta = value - datetime.date.today() 
#     return delta.days >= 0