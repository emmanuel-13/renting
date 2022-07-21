from itertools import count
from msilib.schema import ListView
from urllib import response
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.db.models import Q, Count
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages
from House.forms import *
from House.models import *
from basket.basket import Basket

# Own imports
from customer.models import *
from House.models import *
from payment.models import BookItem, Payment
from .forms import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django_pandas.io import read_frame
from django.http import JsonResponse
from django.http import Http404


def home(request):
    city = City.objects.all()[:8]
    estate = Room.objects.filter(active=False).order_by('date_added')[:4]
    room = Estate.objects.filter(is_featured=True).order_by('date_added')[:3]

    # new_estate = []
    # rooms = Room.objects.all()
    # for rooms in rooms:
    #     new_estate.append(rooms.apartment_name_rooms)
    
    # estates = Estate.objects.all()
    # for estates in estates:
    #     if estates.estate_name in new_estate:
    #         print(estates.id)
    #         new_estate.append(estates.id)
    #     else:
    #         pass
    
                
    

    if request.method == "POST":
        email = request.POST.get('email')
        try:
            if Subscribers.objects.filter(email=email).first():
                messages.info(request, "email already taken")
                return redirect('home')
            
            subscriber = Subscribers.objects.create(email=email)
            subscriber.save()
            message = messages.success(request, 'thank you for subscribing')
            response = JsonResponse({'msg': message })
            return response
        except Exception as e:
            print(e)
        
    context = {
        'city': city, 'estate': estate, 'room': room
    }
    return render(request, 'index.html', context)

@login_required
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            subject = form.cleaned_data.get('subject')
            content = form.cleaned_data.get('content')
            
            messages.success(request, 'infomation send successfully')
            send_mail_user(email, subject)
            return redirect('contact')
        else:
            messages.error(request, 'invalid credentials')                      
    else:
        form = ContactForm()

    context = {
        'form': form
    }
    return render(request, 'contact.html', context)


def send_mail_user(email, subject):
    subject = "New Rent4Less Automation"
    message = f'hi {email} we have receive your mail on the subject {subject} and we would \
                        get back to you as soon as possible for futher informations please \
                            do well to reach out to us on the following lines 0700-25742-6323'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = {email}
    send_mail(subject, message, email_from, recipient_list)
    
# @login_required
# def profile_view(request, username):
#     user_profile = User.objects.get(username=request.user.username)
#     # user_profile = UserProfile.objects.get(user=request.user)
#     profiles = Profile.objects.get(user=user_profile)
    
#     return render(request, 'profile.html', {'pro': profiles})

def check_profile_owner(request, owner):
    if request.user != owner:
        raise Http404

@login_required
def profile_edit(request, username):
    profiles = Profile.objects.get(user=request.user)
    
    check_profile_owner(request, profiles.user)
    if request.method == "POST":
        profile = ProfileEdit(request.POST, request.FILES, instance=request.user.profile)
        form = UserEdit(request.POST, instance=request.user)
        
        if form.is_valid() and profile.is_valid():
            form.save()
            profile.save()
            
            username = form.cleaned_data.get('username')
            emails = form.cleaned_data.get('email')
            title = profile.cleaned_data.get('title')
            
            subject="rent4less Automated messages for profile update"
            email_template_name = "textfile/profile_email.txt"
            c = {
            "email": emails,
            "username": username,
            "title": title,
            'site_name': 'Rent4Less',
            'protocol': 'http',
            }
            email = render_to_string(email_template_name, c)
            try:
                send_mail(subject, email, 'emmysoln@gmail.com' , [emails], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            
            messages.success(request, 'profile updated successfully')
            return redirect(reverse('profile_edit', kwargs={'username': request.user.username}))
    else:
        profile = ProfileEdit(instance=request.user.profile)
        form = UserEdit(instance=request.user)
    
    return render(request, 'profile-edit.html', {'form': form, 'profile': profile})

@login_required(login_url='login')
def user_bookings(request):
    if request.user.is_authenticated == False:
        return redirect('login')
    
    booking = BookItem.objects.all()
        
    user_first = User.objects.all().get(id=request.user.id)
    user = UserProfile.objects.get(user=user_first)
    bookings = BookItem.objects.filter(status=True, payment__username=request.user)
    print(f"request user id ={request.user.id}")

    return render(request, 'mybookings.html', {'bookings': bookings, 'booking': booking})


@login_required(login_url='login')
def user_payment(request):
    if request.user.is_authenticated == False:
        return redirect('login')
    
    booking = Payment.objects.filter(status=True)
    print(f"request user id ={request.user.id}")

    return render(request, 'user_payment.html', {'booking': booking})

@login_required(login_url='login')
def user_form(request):
    if request.user.is_authenticated == False:
        return redirect('login')
    
    user = Profile.objects.filter(user__is_active=True, user__is_staff=False)
    return render(request, 'user_form.html', {'users': user})



from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
from .models import *
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import datetime

class LandLordList(LoginRequiredMixin, ListView):
    model = LandLord
    template_name = "user_form.html"
    context_object_name = "landlord"
    

@login_required(login_url='login')
def landlord_view(request, id):
    if request.user.is_authenticated == False:
        return redirect('login')
    
    profile = LandLord.objects.get(id=id)
    return render(request, 'profile.html', {'landlord': profile})
    

@login_required(login_url='login')
def user_form_view(request, id):
    if request.user.is_authenticated == False:
        return redirect('login')
    
    profile = Profile.objects.get(id=id)
    return render(request, 'profile.html', {'pro': profile})

@login_required(login_url='login')
def booking_views(request, id):
    if request.user.is_authenticated == False:
        return redirect('login')
    
    profile = BookItem.objects.get(id=id)
    return render(request, 'profile.html', {'book': profile})


@login_required(login_url='login')
def make_vacant(request, id):
    if request.user.is_authenticated == False:
        return redirect('login')
    
    profile = BookItem.objects.get(id=id)
    profile.room.occupied = "available"
    profile.room.active = True
    profile.room.save()
    profile.delete()
    
    return redirect('user_booking')
    

@login_required(login_url='login')
def user_dashboard(request):
    profile = Profile.objects.get(user=request.user)
    user_first = User.objects.all().get(id=request.user.id)
    user = UserProfile.objects.get(user=user_first)
    booking = BookItem.objects.filter(status=True, payment__username=request.user).count()
    bookings = BookItem.objects.filter(status=True, payment__username=request.user).order_by('-book_date')
    room = BookItem.objects.filter(status=True, payment__username=request.user).first()
    subscriber = Subscribers.objects.all()
    admin_messages = AdminMessage.objects.all().order_by('-date_created')[:2]
    dev = DevelopmentMessage.objects.all().order_by('-date_created')[:2]
    mails = MailMessage.objects.all().order_by('-date_created')[:2]
    
    print(f"request user id ={request.user.id}")
    
    return render(request, 'user_dashboard.html', {
        'users': user, 'booking': booking, 'bookings': bookings, 'profile': profile, 'room': room,
        'subscriber': subscriber, 'mail': mails, 'admin_messages': admin_messages, 'admin': dev
    })


def error_500(request):
    return render(request, '500.html', status=500)


def error_404(request, exception):
    return render(request, '404.html', status=404)
#
#
# def history(request):
#     try:
#         booking = RoomBooking.objects.get(request.session["booking"])
#     except (KeyError, RoomBooking.DoesNotExist):
#         booking = None
#     return render(request, 'user_history.html', {'booking': booking})


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Rent4Less',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'rent4less@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("password_reset_done")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})


from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, logout, login


# Create your views here.
def login_attempt(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, 'username don\'t exists')
            return redirect('login')

        profile_obj = UserProfile.objects.filter(user=user_obj).first()
        if profile_obj.is_verified is None:
            messages.success(request, 'profile is not verified, please check your mail')
            return redirect('login')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.info(request, 'username or password incorrect')
            return redirect('login')

        login(request, user)
        if user.username == "admin2":
            pass
        else:
            send_mail(subject="recent login ", message=f"{user.username}  just login now", from_email=request.user.email, recipient_list=['emmysoln@gmail.com'])
        return redirect('home')

    return render(request, 'logining.html')


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")


def register_attempt(request):
    if request.method == "POST":
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        status = request.POST.get('status')

        try:
            if User.objects.filter(username=username).first():
                messages.success(request, 'username is taken')
                return redirect('register')

            if User.objects.filter(email=email).first():
                messages.success(request, 'email is taken')
                return redirect('register')

            if status == "staff":
                user_obj = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name, is_staff=True)
                user_obj.set_password(password)
                user_obj.save()

            else:
                user_obj = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name, is_active=True)
                user_obj.set_password(password)
                user_obj.save()
                
            auth_token = str(uuid.uuid4())
            print(auth_token)
            profile_obj = UserProfile.objects.create(user=user_obj, auth_token=auth_token)
            profile_obj.save()

            send_mail_register(email, auth_token)
            return redirect('token')

        except Exception as e:
            print(e)

    return render(request, 'signup.html')


def verify(request, auth_token):
    try:
        profile_obj = UserProfile.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Email Already verified')
                return redirect('login')

            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Email verified please login')
            return redirect('login')
        else:
            return redirect('error')
    except Exception as e:
        print(e)


def error(request):
    return render(request, 'error.html')


@login_required(login_url="login")
def success_attempt(request):
    return render(request, 'success.html')


def token_send(request):
    return render(request, 'token.html')


def send_mail_register(email, token):
    subject = "Account Verification"
    email_template_name = "textfile/verification.txt"
    c = {
    "email": email,
    "token": token,
    'site_name': 'Rent4Less',
    'protocol': 'http',
    }
    email = render_to_string(email_template_name, c)
    try:
        send_mail(subject, email, settings.EMAIL_HOST_USER, recipient_list=[{email}], fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')


def property(request):
    room = Room.objects.filter(active=False)

    context = {
        'room': room
    }
    return render(request, 'properties.html', context)


def property_details(request, pk):
    city = get_object_or_404(City, pk=pk)
    estate = City.objects.all()[:10]
    city_list = City.objects.all()[:6]
    
    main_estate = Estate.objects.filter(city=city)
    
    # mainly = []
    # main = Estate.objects.all()
    # for main in main:
    #     mainly.append(main.estate_name)
    # print(mainly)
        
    apartment = Apartment.objects.all()
    
    apart = []
    for apartment in apartment:
        apart.append(apartment)
    print(apart)
    
    
    mainly = []
    myestate = Estate.objects.all()
    
    for myestate in myestate:
        if myestate.city == city:
            pass
        else:
            mainly.append(myestate)
    
    citys = City.objects.filter(status=0).values_list('citys', flat=True)
    citys = list(citys)

    if main_estate:
        pass
    else:
        messages.info(request, "no estate in that location please try another city")
        return redirect('home')

    context = {
        'estate': estate, 'city': city, 'city_list': city_list, 'main_estate': main_estate, 'mainly': mainly, 'apart': apart
    }
    return render(request, 'listings.html', context)


def email_verify(request):
    if request.method == "POST" and request.is_ajax():
        email = request.POST.get('email', None)
        try:
            if Subscribers.objects.filter(email=email).first():
                response = {
                         'msg': 'Already a subsciber try another one' # response message
                }
            else:
                subscriber = Subscribers.objects.create(email=email)
                subscriber.save()
                response = {
                         'msg':f'thank you for subscribing {subscriber.email}' # response message
                }
            return JsonResponse(response)
    
        except Exception as e:
            print(e)
    return JsonResponse({"success":False}, status=400)

import json

def apartment_details(request, estate_name):
    estate = get_object_or_404(Estate, estate_name=estate_name)
    
    room = Room.objects.filter(apartment_name_rooms=estate.estate_name)
    apartment = Apartment.objects.filter(estate_name=estate.estate_name)[:4]
    city = City.objects.get(citys=estate.city)
    
    
    room_exclusive_1 = Room.objects.filter(apartment_name_rooms=estate.estate_name, apartment_type="X", occupied='available', active=False, bedroom_type="1").first()
    room_exclusive_count_1 = Room.objects.filter(apartment_name_rooms=estate.estate_name, apartment_type="X", occupied='available', active=False, bedroom_type="1").count()
    
    room_exclusive = Room.objects.filter(apartment_name_rooms=estate.estate_name, apartment_type="X", occupied='available', active=False, bedroom_type="2").first()
    room_exclusive_count = Room.objects.filter(apartment_name_rooms=estate.estate_name, apartment_type="X", occupied='available', active=False, bedroom_type="2").count()
    
    room_exclusive_3 = Room.objects.filter(apartment_name_rooms=estate.estate_name, apartment_type="X", occupied='available', active=False, bedroom_type="3").first()
    room_exclusive_count_3 = Room.objects.filter(apartment_name_rooms=estate.estate_name, apartment_type="X", occupied='available', active=False, bedroom_type="3").count()
    
    room_exclusive_4 = Room.objects.filter(apartment_name_rooms=estate.estate_name, apartment_type="X", occupied='available', active=False, bedroom_type="4").first()
    room_exclusive_count_4 = Room.objects.filter(apartment_name_rooms=estate.estate_name, apartment_type="X", occupied='available', active=False, bedroom_type="4").count()
    
    room_exclusive_5 = Room.objects.filter(apartment_name_rooms=estate.estate_name, apartment_type="X", occupied='available', active=False, bedroom_type="5").first()
    room_exclusive_count_5 = Room.objects.filter(apartment_name_rooms=estate.estate_name, apartment_type="X", occupied='available', active=False, bedroom_type="5").count()
    
    
    
    
    room_executives_1 = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Executives", apartment_type="S", occupied='available', active=False, bedroom_type="1").first()
    room_executives_count_1 = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Executives", apartment_type="S", occupied='available', active=False, bedroom_type="1").count()
    
    room_standard_1 = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Standard", apartment_type="S", occupied='available', active=False, bedroom_type="1").first()
    room_standard_count_1 = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Standard", apartment_type="S", occupied='available', active=False, bedroom_type="1").count()
    
    room_deluxe_1 = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Deluxe", apartment_type="S", occupied='available', active=False, bedroom_type="1").first()
    room_deluxe_count_1 = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Deluxe", apartment_type="S", occupied='available', active=False, bedroom_type="1").count()
    
    room_mini_1 = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Mini", apartment_type="S", occupied='available', active=False, bedroom_type="1").first()
    room_mini_count_1 = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Mini", apartment_type="S", occupied='available', active=False, bedroom_type="1").count()
    
    
    #two
    
    room_executives = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Executives", apartment_type="S", occupied='available', active=False, bedroom_type="2").first()
    room_executives_count = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Executives", apartment_type="S", occupied='available', active=False, bedroom_type="2").count()
    
    room_standard = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Standard", apartment_type="S", occupied='available', active=False, bedroom_type="2").first()
    room_standard_count = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Standard", apartment_type="S", occupied='available', active=False, bedroom_type="2").count()
    
    room_deluxe = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Deluxe", apartment_type="S", occupied='available', active=False, bedroom_type="2").first()
    room_deluxe_count = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Deluxe", apartment_type="S", occupied='available', active=False, bedroom_type="2").count()
    
    room_mini = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Mini", apartment_type="S", occupied='available', active=False, bedroom_type="2").first()
    room_mini_count = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Mini", apartment_type="S", occupied='available', active=False, bedroom_type="2").count()
    
    #three
    
    room_executives_3 = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Executives", apartment_type="S", occupied='available', active=False, bedroom_type="3").first()
    room_executives_count_3 = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Executives", apartment_type="S", occupied='available', active=False, bedroom_type="3").count()
    
    room_standard_3 = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Standard", apartment_type="S", occupied='available', active=False, bedroom_type="3").first()
    room_standard_count_3 = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Standard", apartment_type="S", occupied='available', active=False, bedroom_type="3").count()
    
    room_deluxe_3 = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Deluxe", apartment_type="S", occupied='available', active=False, bedroom_type="3").first()
    room_deluxe_count_3 = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Deluxe", apartment_type="S", occupied='available', active=False, bedroom_type="3").count()
    
    room_mini_3 = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Mini", apartment_type="S", occupied='available', active=False, bedroom_type="3").first()
    room_mini_count_3 = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Mini", apartment_type="S", occupied='available', active=False, bedroom_type="3").count()
    
    
    #four
    room_executives_4 = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Executives", apartment_type="S", occupied='available', active=False, bedroom_type="4").first()
    room_executives_count_4 = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Executives", apartment_type="S", occupied='available', active=False, bedroom_type="4").count()
    
    room_standard_4 = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Standard", apartment_type="S", occupied='available', active=False, bedroom_type="4").first()
    room_standard_count_4 = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Standard", apartment_type="S", occupied='available', active=False, bedroom_type="4").count()
    
    room_deluxe_4 = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Deluxe", apartment_type="S", occupied='available', active=False, bedroom_type="4").first()
    room_deluxe_count_4 = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Deluxe", apartment_type="S", occupied='available', active=False, bedroom_type="4").count()
    
    room_mini_4 = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Mini", apartment_type="S", occupied='available', active=False, bedroom_type="4").first()
    room_mini_count_4 = Room.objects.filter(apartment_name_rooms=estate.estate_name, room_types="Mini", apartment_type="S", occupied='available', active=False, bedroom_type="4").count()
    
    
    if apartment:
        pass
    else:
        messages.info(request, "no room availabe here")
        return redirect(reverse('property_detail', kwargs={'pk': city.pk }))
    
    estates = Estate.objects.all()[:6]
    
    new_estate = []
    for estates in estates:
        if estates == estate:
            pass
        else:
            new_estate.append(estates)

    context = {
        'room': room, "estate": estate, 'city': city, 'apartment': apartment, 
        'room_exclusive_1': room_exclusive_1, "room_exclusive_count_1": room_exclusive_count_1,
        'room_exclusive': room_exclusive, 'room_exclusive_3': room_exclusive_3,
        'room_exclusive_4': room_exclusive_4,'room_exclusive_5': room_exclusive_5,
        'room_executives': room_executives, 'room_standard': room_standard, 
        'room_mini': room_mini, 'room_deluxe': room_deluxe,
        'room_exclusive_count': room_exclusive_count, 'room_exclusive_count_3': room_exclusive_count_3, 
        'room_exclusive_count_4': room_exclusive_count_4, 'room_exclusive_count_5': room_exclusive_count_5,
        'room_executives_count': room_executives_count, 
        'room_standard_count': room_standard_count, 'room_deluxe_count': room_deluxe_count, 
        'room_mini_count': room_mini_count, 'estates': new_estate,
        
        'room_executives_4':room_executives_4,
       ' room_executives_count_4':room_executives_count_4,
        'room_standard_4':room_standard_4,
        'room_standard_count_4':room_standard_count_4,
        'room_deluxe_4':room_deluxe_4,
        'room_deluxe_count_4':room_deluxe_count_4,
        'room_mini_4':room_mini_4,
        'room_mini_count_4':room_mini_count_4,
        
        
        'room_executives_1':room_executives_1,
       ' room_executives_count_1':room_executives_count_1,
        'room_standard_1':room_standard_1,
        'room_standard_count_1':room_standard_count_1,
        'room_deluxe_1':room_deluxe_1,
        'room_deluxe_count_1':room_deluxe_count_1,
        'room_mini_1':room_mini_1,
        'room_mini_count_1':room_mini_count_1,
        
        'room_executives':room_executives,
       ' room_executives_count':room_executives_count,
        'room_standard':room_standard,
        'room_standard_count':room_standard_count,
        'room_deluxe':room_deluxe,
        'room_deluxe_count':room_deluxe_count,
        'room_mini':room_mini,
        'room_mini_count':room_mini_count,
        
        'room_executives_3':room_executives_3,
       ' room_executives_count_3':room_executives_count_3,
        'room_standard_3':room_standard_3,
        'room_standard_count_3':room_standard_count_3,
        'room_deluxe_3':room_deluxe_3,
        'room_deluxe_count_3':room_deluxe_count_3,
        'room_mini_3':room_mini_3,
        'room_mini_count_3':room_mini_count_3
    }
    return render(request, 'single.html', context)


def property_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    apartment = Apartment.objects.get(flat_id=room.flat_id_rooms)
    estate = Estate.objects.get(estate_name=apartment.estate_name)
    city = City.objects.get(citys=estate.city)

    context = {
        'room': room, 'apartment': apartment, 'estate': estate, 'city': city
    }
    return render(request, 'property_room.html', context)


def about(request):
    about = About.objects.all()
    context = {
        'about': about
    }
    return render(request, 'about.html', context)

def city(request):
    city = City.objects.all()
    estate = Estate.objects.all()
    estates = Estate.objects.all().order_by('date_added')[:15]
    return render(request, 'citys.html', {'city': city, 'estate': estate, 'estates': estates})

def EstateListAjax(request):
    city = City.objects.filter(status=0).values_list('citys', flat=True)
    citylist = list(city)

    return JsonResponse(citylist, safe=False)


def search(request):
    if request.method == "POST":
        city_search = request.POST.get('search')

        if city_search == "":
            return redirect(request.META.get('HTTP_REFERER'))

        else:
            city = City.objects.filter(citys__icontains=city_search).first()

            if city:
                return redirect("/customer/property/"+str(city.pk))
            else:
                messages.info(request, 'no property matches your search')
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))


def cookie_session(request):
    request.session.set_test_cookie()
    return HttpResponse('<h2> rent for less </h2>')


def delete_cookie(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        response = HttpResponse('rentforless cookie created')
    else:
        response = HttpResponse("rentforless <br> your browser doesn't support cookies ")
    return response
   
   
@staff_member_required
@login_required
def mail_view(request):
    subscriber = Subscribers.objects.all()
    df = read_frame(subscriber, fieldnames=['email'])
    mail_list = df['email'].values.tolist()
    print(mail_list)
    if request.method == "POST":
        form = Mails(request.POST)
        
        if form.is_valid():
            form.save()
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            send_mail(
                message=content,
                subject=title,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list= mail_list,
                fail_silently=False
            )
            messages.info(request, 'mail sent successfully')
            return redirect('mails')

        else:
            messages.success(request, 'mail not sent')
            return redirect('mails')
    
    else:
        form = Mails()
    
    return render(request, 'Dashboard/mail.html', {'form': form})

def send_mail_user_landlord(email, landlord):
    subject = "Landlord Update"
    message = f'{landlord.first_name} with {landlord.phone_no} just requested for a property listing in {landlord.location_of_property}'
    email_from = {email}
    recipient_list = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, recipient_list)

def landlord_create(request):
    if request.method == "POST":
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        location = request.POST.get('location')
        flat = request.POST.get('flat')
        room = request.POST.get('room')
        description = request.POST.get('description')
        
        
        try:
            if LandLord.objects.exists():
                pass
            
            landlord = LandLord.objects.create(first_name=first_name, last_name=last_name, email=email, address=location, 
                                               phone_no=phone, location_of_property=address, number_of_flat=flat, 
                                               number_of_rooms=room, description_of_property=description)
            landlord.save()
            
            messages.info(request, "request submitted successfully")
            send_mail_user_landlord(email, landlord)
            return redirect('home')
        except Exception as e:
            print(e)
    return render(request, 'landlord.html')

