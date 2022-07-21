from django.urls import path
from django.views.generic import TemplateView
from .views import *
from django.contrib.auth import views as auth_views
from House.views import room_updater

urlpatterns = [
    path('login/', login_attempt, name='login'),
    path('register/', register_attempt, name='register'),
    path('success/', success_attempt, name='success'),
    path('token/', token_send, name='token'),
    path('verify/<auth_token>/', verify, name='verify'),
    path('error/', token_send, name='error'),
    path('logout/', logout_request, name='logout'),
    path('contact/', contact, name="contact"),

    #user dasboard
    path('user/dashboard', user_dashboard, name="user_dashboard"),
    path('user/bookings', user_bookings, name="user_booking"),
    path('user/payment', user_payment, name="user_payment"),
    path('profile/<username>/', profile_edit, name="profile_edit"),

    #home page
    path('property/', property, name="property"),
    path('property/<pk>', property_details, name='property_detail'),
    # path('property/estate_name/<id>/', estate_details, name='estate_detail'),
    path('property/estate/<estate_name>/', apartment_details, name='apartment_detail'),
    path('property-rooms/<pk>/rooms', property_room, name='property_rooms'),
    path('email_verify/', email_verify, name="email_verify"),
    path('about/', about, name="about"),
    path('city/', city, name="city"),

    #function ajax
    path('estate_listing', EstateListAjax, name="estate-listing"),
    path('search', search, name="estate-search"),
    
    #lord create
    path('landlord/listing/', landlord_create, name="landlord_create"),
    
    
    
    #newletters
    path('mail', mail_view, name="mails"),
    
    #user docs
    path('users/', user_form, name='user_form'),
    path('users/<id>', user_form_view, name='user_form_view'),
    path('landlord/', LandLordList.as_view(), name='landlord_form'),
    path('landlord/<id>', landlord_view, name='landlord_view'),
    path('bookings/<id>', booking_views, name='booking_views'),
    path('make-vacant/<id>', make_vacant, name='make_vacant'),
    
    #password configurations
    #path('accounts/', include('django.contrib.auth.urls')),
    path("password_reset", password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),      

]
