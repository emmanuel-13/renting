from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('estate_create/', EstateCreate.as_view(), name="estate_create"),
    # path('<pk>/update/', EstateUpdate.as_view(), name="estate_update"),
    path('estate_list/', EstateListView.as_view(), name="estate_list"),
    path('<estate_name>/', estate_detail, name='estate_detailing'),
    path('estate_edit/edit', EstateEdit.as_view(), name='estate_edit'),
    path('estate_delete/<pk>', EstateDeleteView, name='estate_delete'),
    path('<estate_id>/<pk>', block_details, name='block_details'),

    #apartment
    path('<flat_id>/rooms/', apartment_room_details, name='room_det'),
    path('<flat_id>/apartment_update/', apartment_update, name='apartment_update'),
    path('apartment/<estate_name>/', apartment_list, name='apartment_list'),
    path('estate/estate_csv/myestatecsv', estate_csv, name='estate_csv'),
    path('apartment/apartment_csv/<estate_name>', apartment_csv, name='apartment_csv'),
    path('room/room_csv/rooms', room_csv, name='room_csv'),
    path('apartment/estate_list/estate-apartment', estate_list, name='estate_listing'),

    #testing apartment
    path('<apartment_pk>/apartment_testing/', apartment_test, name='apartment_test'),
    path('apartment/<flat_id>/apartd', apartment_room_test, name='apartment_room_test'),

    #rooms
    path('rooms/<room_id>/rooms', room_update, name='room_update'),
    path('rooms/<room_id>/', room_update2, name='room_update2'),
    path('rooms/<room_id>/rooms_detail', room_detail, name='room_detail'),
    path('rooms/<room_pk>/rooms_detail_main', room_detail_main, name='room_details'),
    path('rooms/rooms_update/<room_pk>', room_update_2, name='room_detail_update'),
    path('rooms/room/exclusive/<room_pk>', room_updater, name='room_detail_updater'),
    path('rooms/rooms_update/shared/<room_pk>', room_update_per_shared, name='room_update_per_shared'),
    path('rooms/room/exclusive/exclusive/<room_pk>', room_updater_per_exclusive, name='room_updater_per_exclusive'),
    path('\\room', room_list, name='room_list'),
    
    # history
    path('estate/history_estate/', user_history_for_estate, name='history_estate'),
    path('user./subscriber/', subscriber, name='subscriber'),
    path('estate_history_clear/clear/', clear_estate_history, name='history_clear'),
    
    #development
    path('development/development/devs', list_messages, name='list_messages'),
    path('development/new_messages/', create_message, name='create_message'),
    path('update_message/<pk>/', update_message, name='update_message'),
    path('delete_message/<pk>/', delete_message, name='delete_message'),
    
    #admin messages
    path('admin/admin_message/devs/messages', admin_messages, name='admin_messages'),
    path('admin/new_messages/', admin_create_message, name='admin_create_message'),
    path('admin_update_message/admin/<id>/', admin_update_message, name='admin_update_message'),
    path('admin_delete_message/admin/<id>/', admin_delete_message, name='admin_delete_message'),
]