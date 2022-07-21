from datetime import date, datetime, timedelta
from locale import currency
from tabnanny import verbose
from urllib import request
from django.db import models
import secrets
from .paystack import Paystack
from customer.models import UserProfile
from House.models import Room, only_digit
from django.contrib.auth.models import User
from django.core.mail import mail_admins, send_mail
from django.conf import settings
from django.utils import timezone


class Payment(models.Model):
    payment_type = (
        ('1', '1 Month'), ('3', '3 Month'), ('6', '6 Month'), ('12', '12 Month')
    )
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    phone_no = models.CharField(max_length=11, null=False, blank=True, validators=[only_digit])
    city = models.CharField(max_length=20, blank=True, null=False, default="")
    state = models.CharField(max_length=20, blank=True, null=False, default="")
    address = models.CharField(max_length=20, blank=True, null=False, default="")
    email = models.EmailField()
    payment_type = models.CharField(max_length=10, choices=payment_type, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    status = models.BooleanField(default=False)
    ref = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)
    postal_code = models.CharField(max_length=20, validators=[only_digit], blank=True, null=False, default="")
    size = models.CharField(max_length=20, validators=[only_digit], blank=True, null=False, default="")
    employer_name = models.CharField(max_length=50, null=True)
    employer_address = models.CharField(max_length=20, blank=True, null=False, default="")
    employer_email = models.EmailField(blank=True, null=False, default="")
    employer_phone = models.CharField(max_length=11, null=False, blank=True, validators=[only_digit])
    guarantor_name = models.CharField(max_length=50, blank=True, null=False, default="")
    occupation = models.CharField(max_length=20, blank=True, null=False, default="")
    guarantor_address = models.CharField(max_length=20, blank=True, null=False, default="")
    guarantor_phone = models.CharField(max_length=11, null=False, blank=True, validators=[only_digit])
    guarantor_email = models.EmailField(blank=True)
    additional_occupant = models.BooleanField(default=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def prices(self):
        rents  = str(int(self.price))
        
        if len(rents) == 1:
            new = rents 
            
        elif len(rents) == 2:
            new = rents 
        
        elif len(rents) == 3:
            new = rents 
                
        elif len(rents) == 4:
            new = rents[0] + ',' + rents[1:]
        elif len(rents) == 5:
            new = rents[0:2] + ',' + rents[2:]
            
        elif len(rents) == 6:
            new = rents[0:3] + ',' + rents[3:]
            
        elif len(rents) == 7:
            new = rents[0] + ',' + rents[1:3] + ',' + rents[3:]
            
        else:
            new = rents
        return new

    class Meta:
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return f"{self.name}"

    def save(self, *args, **kwargs) -> None:
        self.price = int(self.price)
        self.prices
        self.list_payment
        try:
            while not self.ref:
                ref = secrets.token_urlsafe(50)
                object_with_similar_ref = Payment.objects.filter(ref=ref)
                if not object_with_similar_ref:
                    self.ref = ref

            super().save(*args, **kwargs)
        except Exception as e:
            print(e)

    def amount_value(self) -> int:
        return self.price * 100

    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.price)
        if status:
            if result['amount'] / 100 == self.price:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False
    
    def list_payment(self):
        paystack = Paystack()
        status, result = paystack.list_payment()
        
        if status == True:
            for result in result:
                if result['customer']['email'] == self.email:
                    email = result['customer']['email']
                    first_name = result['customer']['first_name']
                    phone = result['customer']['phone']
                    customer_code = result['customer']['customer_code']
                    reference = result['reference']
                    if reference == self.ref:
                        amount = result['amount'] / 100
                        channel = result['channel']
            if Payment_list.objects.filter(email=email).first():
                pass
            else:
                Payment_list.objects.create(email=email, name=first_name, phone=phone, customer_code=customer_code, reference=reference, 
                                            status=True)
            return email
            

        else:
            print('no valid status')


class BookItem(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=1)
    status = models.BooleanField(default=False)
    book_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    
    
    def show_room(self):
        return self.room.unique_room_id
    
    def get_current_date(self):
        return timezone.now()
    
    
    
    
    
    def checkout(self):
        
        if self.payment.payment_type == "1":
            self.expiry_date = self.book_date + timedelta(days=30)
            
            if self.expiry_date > timezone.now():
                self.room.occupied = "running"
                self.room.active = True
                self.status = True
                self.room.save()
                print(timezone.now())
                print('yes yes')
            else:
                self.room.occupied = "expired"
                self.room.active = False
                self.status = False
                self.room.save()
                print('no')
            
            
        elif self.payment.payment_type == "3":
            self.expiry_date = self.book_date + timedelta(days=90)
            
            if self.expiry_date > timezone.now():
                self.room.occupied = "running"
                self.room.active = True
                self.status = True
                self.room.save()
                print(timezone.now())
                print('yes yes')
            else:
                self.room.occupied = "expired"
                self.room.active = False
                self.status = False
                self.room.save()
                print('no')
            
        elif self.payment.payment_type == "6":
            self.expiry_date = self.book_date + timedelta(180)
            
            if self.expiry_date > timezone.now():
                self.room.occupied = "running"
                self.room.active = True
                self.status = True
                self.room.save()
                print(timezone.now())
                print('yes yes')
            else:
                self.room.occupied = "expired"
                self.room.active = False
                self.status = False
                self.room.save()
                print('no')
        
        elif self.payment.payment_type == "12":
            self.expiry_date = self.book_date + timedelta(days=360)
            
            if self.expiry_date > timezone.now():
                self.room.occupied = "running"
                self.room.active = True
                self.status = True
                self.room.save()
                print(timezone.now())
                print('yes yes')
            else:
                self.room.occupied = "expired"
                self.room.active = False
                self.status = False
                self.room.save()
                print('no')
            
        else:
            pass
        return self.expiry_date
    
    def months(self):
        return f"{self.payment.payment_type} Months"
    
    def room_price(self):
        listed = str(int(self.room.room_price))
        
        if len(listed) == 1:
            new = "NGN" + listed 
            
        if len(listed) == 2:
            new = "NGN" + listed 
            
        if len(listed) == 3:
            new = "NGN" + listed 
            
        elif len(listed) == 4:
            new ="NGN" + listed[0] + ',' + listed[1:]
        elif len(listed) == 5:
            new = "NGN" + listed[0:2] + ',' + listed[2:]
            
        elif len(listed) == 6:
            new = "NGN" + listed[0:3] + ',' + listed[3:]
            
        elif len(listed) == 7:
            new = "NGN" + listed[0] + ',' + listed[1:3] + ',' + listed[3:]
            
        else:
            new = "NGN" + listed
        return new
    
    class Meta:
        verbose_name_plural = "Bookings"
        verbose_name = "Booking"
    
    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.price)
        if status:
            if result['amount'] / 100 == self.price:
                self.status = True
            self.save()
        if self.status:
            return True
        return False
    
    def __str__(self):
            return str(self.id)
        
    def book_by(self):
        return f'{self.payment.username}'
    
    def room_status(self):
        if self.status == False:
            self.room.active = False
            self.room.occupied = "expired"
            self.room.save()
            
        else:
            self.room.active = True
            self.room.occupied = "running"
            self.room.save()
            
        return f'{self.room.occupied}'
    
    def prices(self):
        payment_price = str(int(self.payment.price))
        if len(payment_price) == 1:
            price = "NGN" + payment_price
        elif len(payment_price) == 2:
            price = "NGN" + payment_price
            
        elif len(payment_price) == 3:
            price = "NGN" + payment_price
            
        elif len(payment_price) == 4:
            price = "NGN" + payment_price[0] + ',' + payment_price[1:]
            
        elif len(payment_price) == 5:
            price = "NGN" + payment_price[0:2] + ',' + payment_price[2:]
            
        elif len(payment_price) == 6:
            price = "NGN" + payment_price[0:3] + ',' + payment_price[3:]
            
        elif len(payment_price) == 7:
            price = "NGN" + payment_price[0] + ',' + payment_price[1:4] + ',' + payment_price[4:]
            
        elif len(payment_price) == 8:
            price = "NGN" + payment_price[0:2] + ',' + payment_price[2:5] + ',' + payment_price[5:]
            
        else:
            price = payment_price
            
        return price
    
    def book_status(self):
        if self.room.occupied == "expired":
            self.status = False
            return self.status
                
        elif self.room.occupied == "terminated":
            self.status = False
            return self.status
            
        elif self.room.occupied == "avaliable":
            self.status = False
            return self.status
            
        elif self.room.occupied == "running":
            self.status = True
            return self.status
    
    def save(self, *args, **kwargs):
        self.book_by
        self.room_status
        self.prices
        self.months
        self.room_price
        self.checkout
        self.book_status
        self.show_room
        
        super().save(*args, **kwargs)

    def get_cost(self):
        return self.price
    

class Payment_list(models.Model):
    email = models.CharField(max_length=50)
    name = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    customer_code = models.CharField(max_length=50, null=True, blank=True)
    amount = models.CharField(max_length=30, null=True, blank=True)
    reference = models.CharField(max_length=50, null=True, blank=True)
    channel = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['email']
        verbose_name_plural = "Payment List"
    
    def __str__(self):
        return self.email
    
    def fetch_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.id)
        if status:
            if result['id'] == self.id:
                result = result['email']
            return result
