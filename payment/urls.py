from django.urls import path
from .views import *

urlpatterns = [
    path('success/', success, name="success"),
    path('list/', list_transaction, name="listed"),
    path('payment/', initiate_payment, name='payment'),
    path('payment/<str:ref>/', verify_payment, name='verify_payment'),
    path('make_payment/', make_payment, name="make_payment"),
    path('user/payment/<username>', list_payment_per_user, name="user_payment")
]
