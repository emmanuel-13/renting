from cgitb import lookup
from codecs import lookup_error
from dataclasses import field
from django import forms
from .models import *
from django.forms import inlineformset_factory
import django_filters
from django.forms import ClearableFileInput
# from image_uploader_widget.widgets import ImageUploaderWidget


class EstateForm(forms.ModelForm):
    
    class Meta:
        model = Estate
        exclude = ('owner',)


BlockFormset = inlineformset_factory(
    Estate, Block, form=EstateForm, extra=1, fields="__all__", can_delete=False, max_num=5
)


# ApartmentImageFormset = inlineformset_factory(
#     Apartment, ApartmentImage, form=ApartmentForm, fields="__all__", extra=1, can_delete=False
# )

class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ("apartment_type", "bedroom_type", "apartment_image",)


class ApartmentFilter(django_filters.FilterSet):
    block = django_filters.AllValuesFilter()
    bedroom_type = django_filters.AllValuesFilter()
    apartment_type = django_filters.AllValuesFilter()

    class Meta:
        model = Apartment
        fields = ['bedroom_type']


class RoomFilter(django_filters.FilterSet):
    apartment_name_rooms = django_filters.AllValuesFilter(lookup_expr='exact')
    blocks = django_filters.AllValuesFilter()
    room_id = django_filters.AllValuesFilter()

    class Meta:
        model = Room
        fields = ["apartment_name_rooms"]
        
class RoomFilterer(django_filters.FilterSet):
    occupied = django_filters.AllValuesFilter(lookup_expr="exact")

    class Meta:
        model = Room
        fields = ["occupied"]


class EstateFilter(django_filters.FilterSet):
    estate_name = django_filters.AllValuesFilter(lookup_expr='exact')
    location = django_filters.AllValuesFilter()
    city = django_filters.AllValuesFilter()

    class Meta:
        model = Estate
        fields = ["city"]


class RoomForm(forms.ModelForm):
    type_rooms = (
        ('Executives', 'executives'), ('Standard', 'standard'), ('Mini', 'mini'), ('Deluxe', 'deluxe')
    )
    
    room_types = forms.ChoiceField(choices = type_rooms)
    
    class Meta:
        model = Room
        fields = ("room_types", "ammenities", "image1", "rent", "power_charge", "service_charge", 'discount')
        
        
class RoomForm2(forms.ModelForm):
    class Meta:
        model = Room
        fields = ("exclusive_room", "image1", "rent", "power_charge", "service_charge", 'discount')

class ApartmentLevel(forms.ModelForm):
    apartment_type = django_filters.AllValuesFilter()
    
    class Meta:
        model = Apartment
        fields = ['bedroom_type']
        

class DevelopmentForm(forms.ModelForm):
    class Meta:
        model = DevelopmentMessage
        fields = ['title', 'description']
        
class AdminForm(forms.ModelForm):
    class Meta:
        model = AdminMessage
        fields = ['title', 'description']
        exclude = ['user']
        
        

