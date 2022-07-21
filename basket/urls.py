from django.urls import path

from . import views

# app_name = 'basket'

urlpatterns = [
    path('display/', views.basket_summary, name='cart_detail'),
    path('add/', views.basket_add, name='cart_add'),
    path('delete/', views.basket_delete, name='basket_delete'),
    # path('update/', views.basket_update, name='basket_update'),
]
