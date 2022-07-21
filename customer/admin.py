from django.contrib import admin
from .models import *
from payment.models import *
from django.contrib.auth.models import User, Group

admin.site.unregister(Group)
    
class UserAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        if request.user.username == "admin2":
            return True
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_view_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj=None):
        if request.user.username == "admin2":
            return True

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_verified']
    list_display_links = ['user']
    list_filter = ['user', 'is_verified']
    search_fields = ['user']
    
    def has_add_permission(self, request, obj=None):
        if request.user.username == "admin2":
            return True
    
    def has_change_permission(self, request, obj=None):
        if request.user.username == "admin2":
            return True
        return False
    
    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser and request.user.is_staff :
            return True
        return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.username == "admin2":
            return True
    
    
@admin.register(LandLord)
class LandLordAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone_no', 'email']
    list_display_links = ['first_name']
    list_filter = ['first_name', 'email', 'phone_no']
    search_fields = ['email', 'phone_no']
    readonly_fields = ['first_name', 'last_name', 'phone_no', 'email', 'address', 'description_of_property', 'location_of_property', 'number_of_flat', 'number_of_rooms']
    
    def has_add_permission(self, request, obj=None):
        if request.user.username == "admin2":
            return True
    
    def has_delete_permission(self, request, obj=None):
        if request.user.username == "admin2":
            return True
        

@admin.register(BookItem)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'book_by', 'show_room', 'room_price', 'prices', 'months', 'book_date', 'checkout', 'book_status', 'room_status']
    list_display_links = ['book_by']
    fieldsets = (
        (None, {
            "fields": (
                ['room']
            ),
        }),
    )
    
    # list_editable = ['book_by']
    
    
    def has_add_permission(self, request, obj=None):
        if request.user.username == "admin2":
            return True
        else:
            return False
    
    def has_view_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj=None):
        if request.user.username == "admin2":
            return True
        return False


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['email', 'subject']
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False
    
    def has_view_permission(self, request, obj=None):
        return False


@admin.register(Subscribers)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'date_subcribe' ]
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['email',]
        
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.username == "admin2":
            return True
        return False
    
    
@admin.register(MailMessage)
class MailMessageAdmin(admin.ModelAdmin):
    list_display = ['title', 'content' ]
    list_filter = ['title']
    search_fields = ['title']
    
    
    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False   
    
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'date_of_birth', 'image']
    list_filter = ['date_of_birth', 'title']
    list_display_links = ['user']
    search_fields = ['user']
    
    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False
    
    def has_add_permission(self, request, obj=None):
        if request.user.username == "admin2":
            return True
    
    def has_change_permission(self, request, obj=None):
        if request.user.username == "admin2":
            return True
    
    
    def has_delete_permission(self, request, obj=None):
        if request.user.username == "admin2":
            return True
        return False
    
admin.site.register(About)