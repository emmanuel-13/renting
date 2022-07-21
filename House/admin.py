from email.headerregistry import Group
from django.contrib import admin
from .models import *
from .forms import *
from django import forms
import csv
from django.http import HttpResponse
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'superuser', 'active', 'staff')
    list_filter = ('superuser', 'active', 'staff')
    readonly_fields = [
        'last_login'
    ]
    
    def has_delete_permission(self, request, obj=None):
        if request.user.username == "admin2":
            return True
        
    def has_add_permission(self, request, obj=None):
        if request.user.username == "admin2" and request.user.is_superuser:
            return True
    


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class EstateImageInline(admin.StackedInline):
    model = EstateImage
    extra = 1
    max_num = 4

class BlockInline(admin.StackedInline):
    model = Block
    extra = 1
    
class EstatePropertyInline(admin.StackedInline):
    model = Estate_property
    extra = 1
    max_num = 1


admin.site.register(City)


@admin.register(Estate)
class EstateAdmin(admin.ModelAdmin):
    list_display = ['estate_name', 'location', 'new_apartment_name', 'date_added', 'city']
    search_fields = ['city']
    inlines = [EstatePropertyInline, EstateImageInline, BlockInline]
    actions = ["export_as_csv"]
    exclude = ['owner']
    
    
    
    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False
        
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser and request.user.is_staff:
            return True
        return False

    def has_view_permission(self, request, obj=None):
        return True
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        obj.save()

@admin.register(Apartment)
class Apartment(admin.ModelAdmin):
    list_display = ['estate_name', 'block', 'flat_id', 'apartment_type', 'bedroom_type']
    list_filter = ['flat_id', 'apartment_type']
    list_per_page = 10

    fieldsets = (
        ("", {
            "fields": (
                ['estate_name', 'block', 'flat_id', 'apartment_type', 'bedroom_type', 'apartment_image']
            ),
        }),
    )   
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        obj.save()

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['estate_name', 'block', 'flat_id']
        else:
            return []

    def has_add_permission(self, request, obj=None):
        if request.user.username == "admin2":
            return True    
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False
        
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser and request.user.is_staff:
            return True
        return False

class RoomAdminInline(admin.StackedInline):
    model = RoomImages
    extra = 1
    max_num = 4

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id','apartment_name_rooms', 'blocks', 'flat_id_rooms', 'room_id', 'unique_room_id', 'new_price', 'price', 'active', 'apartment_type', 'occupied']
    list_editable = ['active', 'occupied']
    list_filter = ['room_id', 'room_types']
    list_display_links = ['apartment_name_rooms']
    list_per_page = 10
    actions = ["export_as_csv"]
    inlines = [RoomAdminInline]
    
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner_room = request.user
        obj.save()
    
    
    def get_fieldsets(self, request, obj=None):
        if obj.apartment_type == "X":
            return [("Room", {
                'fields': ([ 'exclusive_room', 'ammenities', 'image1', 'rent', 'service_charge',
                            'power_charge', 'discount'])
            })]
        return [("Room", {
                'fields': (['room_types', 'ammenities', 'image1', 'rent', 
                            'service_charge', 'power_charge', 'discount'])
                })]
        
    def get_form(self, request, obj=None, **kwargs):
        if obj.apartment_type == "X":
            defaults = {'exclude': ('room_types',)}
        else:
            defaults = {'exclude': ('exclusive_room',)}
        
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.apartment_type == "S":
                return ['blocks', 'room_id', 'apartment_name_rooms', 'bedroom_type']
            else:
                return ['blocks', 'room_id', 'apartment_name_rooms', 'bedroom_type', 'exclusive_room']
        else:
            return []

    def has_add_permission(self, request, obj=None):
        if request.user.username == "admin2":
            return True
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False
        
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False


admin.site.register(Testemonial)

@admin.register(AdminMessage)
class AdminMessages(admin.ModelAdmin):
    list_display = ['user' ,'title', 'date_created', 'update_at']
    fieldsets = (
        (None, {
            "fields": (
                ['new_name', 'title', 'date_created', 'description']
            ),
        }),
    )
    

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False
        
    def has_add_permission(self, request, obj=None):
        return False
    
    def get_readonly_fields(self, request, obj=None):
            return ['new_name', 'title', 'date_created', 'update_at', 'description']
        
    