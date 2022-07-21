from ctypes import addressof
from distutils.command.upload import upload
from email import message
import email
from email.headerregistry import Address
from django.contrib.auth.models import User
from django.db import models
from House.models import *
from django.core.mail import send_mail
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

   
def only_digit(value):
    if value.isdigit()==False:
        raise ValidationError('Can only contain numbers')
    
    
     
class Profile(models.Model):
    title_type = (
        ('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Master', 'Master'), ('Chief', 'Chief'), ('Bachelor', 'Bachelor'), ('Prof', 'Prof')
    )
    
    title = models.CharField(max_length=10, choices=title_type, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(auto_now=False, null=True)
    image = models.ImageField(upload_to='profile/', default="download.jpg")
    phone_no = models.CharField(max_length=11, null=True, blank=True, validators=[only_digit])
    address = models.CharField(max_length=50, null=True, blank=True)
    
    
    def __str__(self):
        return self.user.username
    
class LandLord(models.Model):
    first_name = models.CharField(max_length=15, null=False)
    last_name = models.CharField(max_length=15, blank=False, null=False)
    phone_no = models.CharField(max_length=11, null=False, blank=False, validators=[only_digit])
    address = models.CharField(max_length=20)
    email = models.EmailField(null=False)
    location_of_property = models.CharField(max_length=50, null=False, blank=False)
    number_of_flat = models.CharField(max_length=2, null=False, blank=False, validators=[only_digit])
    number_of_rooms = models.CharField(max_length=2, null=False, blank=False, validators=[only_digit])
    description_of_property = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    
    

class Contact(models.Model):
    email = models.EmailField(unique=True)
    subject = models.CharField(max_length=50)
    content = models.TextField()

    def __str__(self):
        return self.subject
    
    
class Subscribers(models.Model):
    email = models.EmailField(null=True)
    date_subcribe = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "Subscriber"
        verbose_name_plural = "Subscribers"

class MailMessage(models.Model):
    
    title = models.CharField(max_length=200, null=True)
    content = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def get_date(self):
        return datetime.today()
    
    def save(self, *args, **kwargs):
        self.get_date
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Mail Message"
        verbose_name_plural = "Mail Messages"
        
        
class About(models.Model):
    title = models.CharField(max_length=50, null=True)
    content = models.TextField()
    
    def __str__(self):
        return self.id
    
    