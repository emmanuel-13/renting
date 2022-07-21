from datetime import datetime
from distutils.command.upload import upload
from email.policy import default
from tabnanny import verbose
from time import timezone
from turtle import update
from django.db import models
import re
from django.urls import reverse
from django.core.validators import RegexValidator
from PIL import Image
from django.core.exceptions import ValidationError
from django.db import transaction
from django.contrib.auth.models import User


def only_digit(value):
    if value.isdigit()==False:
        raise ValidationError('Can only contain numbers')


class City(models.Model):
    
    citys = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to='city', blank=True, null=True)
    status = models.CharField(default=0, editable=False, max_length=1)

    def __str__(self):
        return self.citys
    
    class Meta:
        verbose_name_plural = "Cities"



class Estate(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    estate_name = models.CharField(max_length=100, unique=True, help_text="enter a valid apartment name",)
    image = models.ImageField(upload_to='uploads/post_photos', blank=False, null=False, default="")
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=40)
    description = models.TextField()
    is_featured = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.estate_name

    def estate_names(self):
        return self.estate_name

    def new_apartment_name(self):
        apartment = self.estate_name
        apartment = str(apartment)

        apartment = re.split('\s+', apartment)

        new = []
        for new_apartment in apartment:
            if len(new_apartment) >= 1:
                new_apartment = new_apartment[0]
                new.append(new_apartment)

        new = "".join(new)
        new = new.upper()
        return new

        
    
    def save(self, *args, **kwargs):
        self.new_apartment_name
        self.estate_name
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        
        if img.height > 450 and img.width > 500:
            output_size = (450, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)

    class Meta:
        verbose_name_plural = "Estates"
        ordering = ("estate_name",)

    def get_absolute_url(self):
        return reverse("apartment_detail", kwargs={"estate_pk": self.estate_pk})

class EstateImage(models.Model):
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='estate/image', blank=True)
    
    def __str__(self):
        return self.estate.estate_name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.images.path)
        
        if img.height > 450 and img.width > 500:
            output_size = (450, 500)
            img.thumbnail(output_size)
            img.save(self.images.path)
        
class Estate_property(models.Model):
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)
    property_detail = models.TextField(null=True, blank=True)
    additional_details = models.TextField(null=True, blank=True)
    feature = models.TextField(null=True, blank=True)
    property_video = models.CharField(max_length=255, null=True, blank=True, default="")
    
    def __str__(self):
        return self.estate.estate_name
    
    
    


class Block(models.Model):
    estate_names = models.ForeignKey(Estate, on_delete=models.CASCADE)
    block_no = models.CharField(max_length=1, null=False, help_text="block number must be in numbers", validators=[only_digit])
    total_flat = models.CharField(max_length=2, null=False, help_text="total flat must be in numbers", validators=[only_digit])

    def __str__(self):
        return self.block_no
    
    # def get_block(self):
    #     estate = Estate.objects.filter(estate_name=self.estate_names)
        
    #     block = Block.objects.filter(estate_names=estate)
        

    @property
    def total_flat_no(self):
        return self.total_flat

    def save(self, *args, **kwargs):
        
        block = self.block_no
        
        self.total_flat_no

        apartment = self.estate_names
        apartments = str(apartment)

        apartments = re.split('\s+', apartments)

        new = []
        for new_apartments in apartments:
            if len(new_apartments) >= 1:
                new_apartments = new_apartments[0]
                new.append(new_apartments)

        new = "".join(new)
        new = new.upper()

        total_flats = int(self.total_flat)

        triple = []
        for i in range(1, (total_flats) + 1):
            signle = new + self.block_no + "|" + str(i)
            triple.append(signle)

        values = triple
        
        apartment = Apartment.objects.filter(block=block, estate_name=self.estate_names)

        apart = []


        for i in values:
            owner = self.estate_names.owner
            estate_name = self.estate_names
            block = self.block_no
            location = self.estate_names.location
            city = self.estate_names.city
            flat = i
            apart.append(Apartment(owner=owner, estate_name=estate_name, block=block, flat_id=flat, location=location, city=city))

        if Apartment.objects.filter(estate_name=self.estate_names).exists():
            apartment.delete()
            Apartment.objects.bulk_create(apart)
        else:
            Apartment.objects.bulk_create(apart)
            
            
        super().save(*args, **kwargs)


class Apartment(models.Model):
    types = (
        ('S', 'Shared Apartment'), ('X', 'Exclusive Apartment')
    )

    flat_types = (
        ('1', '1 Bedroom Flat'), ('2', '2 Bedroom Flat'), ('3', '3 Bedroom Flat'), ('4', '4 Bedroom Flat'), ('5', '5 Bedroom Flat')
    )
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    estate_name = models.CharField(max_length=20, null=True, blank=True)
    block = models.CharField(max_length=20, null=True, blank=True)
    flat_id = models.CharField(max_length=20, null=True, blank=True)
    apartment_type = models.CharField(max_length=20, choices=types, default=[0][0])
    bedroom_type = models.CharField(max_length=20, choices=flat_types, default="1")
    apartment_image = models.ImageField(upload_to='apartment/', null=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.flat_id

    class Meta:
        ordering = ("flat_id",)

    def save(self, *args, **kwargs):

        self.block
        self.estate_name
        flat_id = self.flat_id

        room = int(self.bedroom_type)

        rooms = []
        for room in range(1, room+1):
            new_list = flat_id + '|' + str(room)
            rooms.append(new_list)
            
        room_exclusive = flat_id + '|' + str(room)

        roomsss = Room.objects.filter(flat_id_rooms=flat_id)
        
        if self.apartment_type == "S":
            

            room_list = []
            for room in rooms:
                room_list.append(Room(owner_room=self.owner, apartment_name_rooms=self.estate_name, blocks=self.block, 
                                    flat_id_rooms=self.flat_id, room_id=room, apartment_type=self.apartment_type,
                                    bedroom_type=self.bedroom_type, image1=self.apartment_image, location=self.location, city=self.city
                                    ))
            
            if Room.objects.exists():
                roomsss.delete()
                Room.objects.bulk_create(room_list)
            else:
                Room.objects.bulk_create(room_list)
        elif self.apartment_type == "X" :
            if Room.objects.filter(apartment_name_rooms=self.estate_name).exists():
                roomsss.delete()
                Room.objects.create(
                    owner_room=self.owner,
                    apartment_name_rooms=self.estate_name, blocks=self.block, 
                    flat_id_rooms=self.flat_id, apartment_type=self.apartment_type,room_id=room_exclusive,
                    bedroom_type=self.bedroom_type, location=self.location, city=self.city
                    )
            else:
                Room.objects.create(
                    owner_room=self.owner,
                    apartment_name_rooms=self.estate_name, blocks=self.block, 
                    flat_id_rooms=self.flat_id, apartment_type=self.apartment_type, room_id=room_exclusive,
                    bedroom_type=self.bedroom_type, location=self.location, city=self.city)
        
        super().save(*args, **kwargs)



class Room(models.Model):
    type_rooms = (
        ('Executives', 'executives'), ('Standard', 'standard'), ('Mini', 'mini'), ('Deluxe', 'deluxe')
    )

    status = (
        ('available', 'available'), ('expired', 'expired'), ('terminated', 'terminated'), ('running', 'running')
    )
    
    types = (
        ('S', 'Shared Apartment'), ('X', 'Exclusive Apartment')
    )

    flat_types = (
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')
    )
    
    type = (
        ('Exclusive', 'Exclusive'),
    )
    
    owner_room = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    apartment_name_rooms = models.CharField(max_length=50, null=True, blank=True)
    blocks = models.CharField(max_length=10, null=True, blank=True)
    flat_id_rooms = models.CharField(max_length=10, null=True, blank=True)
    apartment_type = models.CharField(max_length=20, choices=types, default=[0][0])
    bedroom_type = models.CharField(max_length=20, choices=flat_types)
    room_id = models.CharField(max_length=20, null=True, blank=True)
    room_types = models.CharField(max_length=15, null=True, blank=True, choices=type_rooms)
    ammenities = models.TextField()
    image1 = models.FileField(upload_to='uploads/post_photos', blank=True, null=True)
    unique_room_id = models.CharField(max_length=20, null=True, editable=True, blank=True)
    rent = models.CharField(max_length=7, help_text="please rent must be in numbers", validators=[only_digit], null=True, blank=True, default=0)
    service_charge = models.CharField(max_length=6, help_text="service charge must be in numbers",validators=[only_digit], null=True, blank=True, default=0)
    power_charge = models.CharField(max_length=6, help_text="power charge must be in numbers", validators=[only_digit], null=True, blank=True, default=0)
    exclusive_room = models.CharField(max_length=20, null=True, blank=True, choices=type, default="Exclusive")
    room_price = models.FloatField(editable=False, default=0, null=True)
    my_new_price = models.FloatField(editable=False, default=0, null=True)
    occupied = models.CharField(default="available", choices=status, max_length=10)
    discount = models.CharField(max_length=2, validators=[only_digit], null=True, blank=True, default=0)
    active = models.BooleanField(default=False)
    location = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=10, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Room'
        abstract = False
        ordering = ("apartment_name_rooms",)

    
    def discounted(self):
        self.my_new_price = self.room_price - ((self.room_price * float(self.discount))/ 100)
        return self.my_new_price
    
    def new_price(self):
        new_price = self.room_price - ((self.room_price * float(self.discount))/ 100)
        listed = str(int(new_price))
        
        if len(listed) == 1:
            new = listed 
            
        elif len(listed) == 2:
            new = listed 
            
        elif len(listed) == 3:
            new = listed 
            
        elif len(listed) == 4:
            new = listed[0] + ',' + listed[1:]
        elif len(listed) == 5:
            new =  listed[0:2] + ',' + listed[2:]
            
        elif len(listed) == 6:
            new =  listed[0:3] + ',' + listed[3:]
            
        elif len(listed) == 7:
            new = listed[0] + ',' + listed[1:3] + ',' + listed[3:]
            
        else:
            new =  listed
        return new

    def room_occupied(self):
        return self.occupied
    
    def service(self):
        rents = self.service_charge
        
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
            
        else:
            new = rents
        return new
    
    def power(self):
        rents = self.power_charge
        
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
            
        else:
            new = rents
        return new
    
    def rented(self):
        rents = self.rent
        
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
    
    def price(self):
        room = int(self.rent) + int(self.power_charge) + int(self.service_charge)
        listed = str(room)
        
        
        if len(listed) == 1:
            new = listed 
            
        elif len(listed) == 2:
            new = listed 
            
        elif len(listed) == 3:
            new = listed 
            
        elif len(listed) == 4:
            new = listed[0] + ',' + listed[1:]
        elif len(listed) == 5:
            new =  listed[0:2] + ',' + listed[2:]
            
        elif len(listed) == 6:
            new =  listed[0:3] + ',' + listed[3:]
            
        elif len(listed) == 7:
            new = listed[0] + ',' + listed[1:3] + ',' + listed[3:]
            
        else:
            new =  listed
        return new
    

    def save(self, *args, **kwargs):
        total_price = int(self.rent) + int(self.power_charge) + int(self.service_charge)
        
        self.room_price = float(total_price)
        self.room_price
        
        self.my_new_price = self.room_price - ((self.room_price * float(self.discount))/ 100)
        self.my_new_price
        
        if self.apartment_type == "S":
            self.unique_room_id = self.room_id + self.room_types[0]
        else:
            self.unique_room_id = self.room_id + self.exclusive_room[0]
            
        self.unique_room_id
            
        self.occupied
        self.price
        self.rented
        self.service_charge
        self.power_charge
        self.new_price

        super().save(*args, **kwargs)

    def __str__(self):
        return self.occupied
    
class RoomImages(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='room_images/', null=True)
    tags = models.TextField(default="still on development")
    
    def __str__(self):
        return self.tags
    
    class Meta:
        verbose_name_plural = "Multiple Room Images"
    

class Testemonial(models.Model):
    name = models.CharField(max_length=20)
    content = models.TextField()
    images = models.ImageField(upload_to='testemonials', null=True, blank=True)

    def __str__(self):
        return self.content

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.images.path)

        if img.height > 450 and img.width > 500:
            output_size = (450, 500)
            img.thumbnail(output_size)
            img.save(self.images.path)


class EstateHistory(models.Model):
    hist_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    estate_id = models.CharField(max_length=100000, default="", null=True)
    date_checked = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.estate_id
    
    class Meta:
        verbose_name_plural = "Estate History's"
        verbose_name = "Estate History"
    
class DevelopmentMessage(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return  self.title
    
    class Meta:
        verbose_name_plural = "Development Messages"
        ordering = ['date_created']


class AdminMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return  self.title
    
    def new_name(self):
        username = self.user
        return username
    
    def get_date(self):
        return timezone.now()
    
    def delete_message(self):
        if self.get_date < self.date_created:
            return True
        else:
            pass
        
    @property
    def get_delete_message(self):
        if self.delete_message:
            new_booking = AdminMessage.objects.filter(date_created__gte=datetime.now())
            for new_booking in new_booking:
                new_booking.delete()
        else:
            pass
    
    def save(self, *args, **kwargs):
        self.new_name
        self.get_date
        self.get_delete_message
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Dev Messages"
        ordering = ['date_created']
        

class MessageCount(models.Model):
    title_count = models.CharField(max_length=3)
    
    def __str__(self):
        return self.title_count
    
    
    

