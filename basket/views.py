from urllib import response
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from House.models import Estate, Room

from .basket import Basket
import json


def basket_summary(request):
    estate = Room.objects.filter(active=False).order_by('date_added')[:8]
    basket = Basket(request)
    return render(request, 'basket/carting.html', {'basket': basket, 'estate': estate})


def basket_add(request):
    basket = Basket(request)
    data = json.loads(request.body)
    roomid = data['roomid']
    action = data['action']
    print('roomid:', roomid)
    print('Action:', action)
    
    room = get_object_or_404(Room, id=roomid)
    basket.add(room=room, qty=1)
    basketqty = basket.__len__()
    response = JsonResponse({'qty': basketqty})
    return response
        
        
def basket_delete(request):
    basket = Basket(request)
    data = json.loads(request.body)
    roomid = data['roomid']
    action = data['action']
    print('roomid:', roomid)
    print('Action:', action)
    basket.delete(room=roomid)
    basketqty = basket.__len__()
    baskettotal = basket.get_total_price()
    response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
    return response

def clear(request):
    basket = Basket()
    basket.clear()
    return JsonResponse("i am passed")


# def basket_update(request):
#     basket = Basket(request)
#     if request.POST.get('action') == 'post':
#         room_id = int(request.POST.get('roomid'))
#         room_qty = int(request.POST.get('roomqty'))
#         basket.update(room=room_id, qty=room_qty)

#         basketqty = basket.__len__()
#         basketsubtotal = basket.get_subtotal_price()
#         response = JsonResponse({'qty': basketqty, 'subtotal': basketsubtotal})
#         return response


