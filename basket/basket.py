from decimal import Decimal

from django.conf import settings
from House.models import Room


class Basket:
    """
    A base Basket class, providing some default behaviors that
    can be inherited or overrided, as necessary.
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def add(self, room, qty):
        """
        Adding and updating the users basket session data
        """
        room_id = str(room.id)

        if room_id in self.basket:
            self.basket[room_id]["qty"] = qty
        else:
            self.basket[room_id] = {"price": str(room.my_new_price), "qty": qty}

        self.save()

    def __iter__(self):
        """
        Collect the product_id in the session data to query the database
        and return products
        """
        room_ids = self.basket.keys()
        rooms = Room.objects.filter(id__in=room_ids)
        basket = self.basket.copy()

        for room in rooms:
            basket[str(room.id)]["room"] = room

        for item in basket.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["qty"]
            yield item

    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        return sum(item["qty"] for item in self.basket.values())


    def update(self, room, qty):
        """
        Update values in session data
        """
        room_id = str(room)
        if room_id in self.basket:
            self.basket[room_id]["qty"] = qty
        self.save()

#for normal
    def subtotals_price(self):
        prices = int(sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values()))
        return prices
  
#for slicing subtotal  
    def get_subtotal_price(self):
        prices = sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())
        
        price = str(int(prices))
        
        if len(price) == 1:
            get_price = price
            
        elif len(price) == 2:
            get_price = price
            
        elif len(price) == 3:
            get_price = price
            
        elif len(price) == 4:
            get_price = price[0] + ',' + price[1:]
            
        elif len(price) == 5:
            get_price = price[0:2] + "," + price[2:]
            
        elif len(price) == 6:
            get_price = price[0:3] + "," + price[3:]
            
        elif len(price) == 7:
            get_price = price[0] + "," + price[1:4] + "," + price[4:]
            
        return get_price
    
#for total_price 
    def get_total_prices(self):
        subtotal = sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())
        

        if subtotal == 0:
            tax = Decimal(0.00)

        else:
            tax = 0.075

        print(tax)
        total = int(subtotal) + (int(subtotal) * tax)
        
        return int(total)
    
#total price slicing
    def get_total_price(self):

        subtotal = sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())

        if subtotal == 0:
            tax = Decimal(0.00)
        else:
            tax = 0.075

        total = int(subtotal) + (int(subtotal) * tax)
        
        
        price = str(int(total))
        
        if len(price) == 1:
            get_price = price
            
        elif len(price) == 2:
            get_price = price
            
        elif len(price) == 3:
            get_price = price
            
        elif len(price) == 4:
            get_price = price[0] + ',' + price[1:]
            
        elif len(price) == 5:
            get_price = price[0:2] + "," + price[2:]
            
        elif len(price) == 6:
            get_price = price[0:3] + "," + price[3:]
            
        elif len(price) == 7:
            get_price = price[0] + "," + price[1:4] + "," + price[4:]
        
        return get_price
    
    
    def delete(self, room):
        """
        Delete item from session data
        """
        room_id = str(room)

        if room_id in self.basket:
            del self.basket[room_id]
            self.save()

    def clear(self):
        # Remove basket from session
        del self.session[settings.BASKET_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True


"""
Code in this file has been inspried/reworked from other known works. Plese ensure that
the License below is included in any of your work that is directly copied from
this source file.


MIT License

Copyright (c) 2019 Packt

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
