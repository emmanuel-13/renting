from django.contrib import admin
from .models import *

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['username', 'phone_no', 'prices', 'created_at', 'status', 'list_payment']
    
    def has_add_permission(self, request, obj=None):
        if request.user.username == "admin2":
            return True
        return False
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser and request.user.is_staff:
            return True
        return False
    
    def has_view_permission(self, request, obj=None):
        return False
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['name', 'username', 'phone_no', 'email', 'payment_type', 'price', 'city', 'status', 'verified', 'ref', 'address', 
                    'state', 'postal_code', 'size', 'employer_name', 'employer_address', 'employer_email',
                    'employer_phone', 'guarantor_name', 'occupation', 'guarantor_phone',
                    'guarantor_address', 'guarantor_email', 'additional_occupant'
                    ]
        
    def has_delete_permission(self, request, obj=None):
        if request.user.username == "admin2":
            return True
        return False
        

# @admin.register(Payment_list)
# class Payment_list(admin.ModelAdmin):
#     list_display = ['email', 'phone', 'name', 'customer_code', 'created_at', 'status']
#     list_per_page = 10
        
#     def has_add_permission(self, request, obj=None):
#         if request.user.username == "admin2":
#             return True
#         return False
    
#     def has_change_permission(self, request, obj=None):
#         if request.user.is_superuser and request.user.is_staff:
#             return True
#         return False
    
#     def has_view_permission(self, request, obj=None):
#         return False
    
#     def get_readonly_fields(self, request, obj=None):
#         if obj:
#             return ['email', 'phone', 'name', 'amount', 'customer_code', 'created_at', 'status', 'channel', 'reference']
        
#     def has_delete_permission(self, request, obj=None):
#         if request.user.username == "admin2":
#             return True

