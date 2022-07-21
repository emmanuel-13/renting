from audioop import reverse
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from .models import *
from django.conf import settings
from django.contrib import messages
from basket.basket import Basket
from customer.models import UserProfile
from django.contrib.auth.decorators import login_required
from fpdf import FPDF
from django.http import FileResponse
from payment.paystack import Paystack
from django.contrib.admin.views.decorators import staff_member_required


def initiate_payment(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        basket = Basket(request)
        if request.method == "POST":
            city = request.POST.get('city')
            phone_no = request.POST.get('phone_no')
            payment_type = request.POST.get('payment-mode')
            address = request.POST.get('address')
            state = request.POST.get('state')
            postal_code = request.POST.get('postal-code')
            size = request.POST.get('check')
            employer_name = request.POST.get('employer-name')
            employer_address = request.POST.get('employer-address')
            employer_email = request.POST.get('employer-email')
            employer_phone = request.POST.get('employer-phone')
            guarantor_name = request.POST.get('Guarantor-name')
            occupation = request.POST.get('Occupation')
            guarantor_address = request.POST.get('Guarantor-address')
            guarantor_phone = request.POST.get('Guarantor-phone_no')
            guarantor_email = request.POST.get('Guarantor-email')
            additional_occupant = request.POST.get('additional-occupant')
            
            try:
                
                pay = Payment.objects.create(
                    name=request.user.first_name, phone_no=phone_no, city=city, email=request.user.email, payment_type=payment_type,
                    price=float(basket.get_total_prices()) * float(payment_type), username=request.user, address=address, state=state, 
                    postal_code=postal_code, size=size, employer_name=employer_name, employer_address=employer_address, employer_email=employer_email,
                    employer_phone=employer_phone, guarantor_name=guarantor_name, occupation=occupation, guarantor_phone=guarantor_phone,
                    guarantor_address=guarantor_address, guarantor_email=guarantor_email, additional_occupant=additional_occupant
                    
                )
            
                return render(request, 'make_payment.html', {
                    'payment': pay, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY
                })

            except Exception as e:
                print(e)
                
        return render(request, 'checkout.html', {'basket': basket})
    else:
        return redirect('login')

@login_required
def verify_payment(request: HttpRequest, ref: str) -> HttpResponse:
    basket = Basket(request)
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    
    if verified:
        for item in basket:
                BookItem.objects.create(
                    payment=payment,
                    room=item['room'],
                    price=item['price'],
                    status=True
                )
        payment.status = True
        payment.save()
        basket.clear()
        messages.success(request, 'payment verify successfully')
        send_mail(subject="Booking Automation Mail", message=f"{payment.username} just made a payment", from_email=f'{payment.email}', recipient_list=['emmysoln@gmail.com'])
    else:
        payment.status = False
        payment.delete()
        payment.save()
        messages.error(request, 'verifcation not complete')
        send_mail(subject="Booking Automation Mail", message=f"{payment.username} just made a payment which is not verified", from_email='emmysoln@gmail.com', recipient_list=[{payment.email}])
    return redirect('success')
    
    
@login_required
@staff_member_required
def list_transaction(request: HttpRequest) -> HttpResponse:
    listed_trans = Payment_list.objects.all()
    return render(request, 'succ.html', {'listed': listed_trans})

@login_required
@staff_member_required
def view_transaction(request: HttpRequest, id: int) -> HttpResponse:
    payment_list = get_object_or_404(Payment_list, id=id)
    check = payment_list.fetch_payment()
    if check:
        return render(request, 'fetch.html')
    else:
        return redirect('listed')

@login_required
def success(request):
    return render(request, 'create.html', {})


@login_required
def make_payment(request):
    payment = get_object_or_404(BookItem, payment__username=request.user.username)
    payment.book_date = payment.payment.updated_at
    if payment.payment.payment_type == "1":
        payment.checkout = payment.book_date + timedelta(30)
    elif payment.payment.payment_type == "3":
        payment.checkout = payment.book_date + timedelta(90)
    elif payment.payment.payment_type == "6":
        payment.checkout = payment.book_date + timedelta(180)
    elif payment.payment.payment_type == "12":
        payment.checkout = payment.book_date + timedelta(360)
    payment.status = True
    payment.room.occupied = True
    payment.room.active = True
    payment.room.save()
    messages.info(request, 'payment_successfull')
    return redirect(reverse('user_booking'))


def list_payment_per_user(request, username):
    payment = Payment.objects.filter(name=request.user.first_name)
    return render(request, 'user_payment.html', {'payment': payment})
    
    
    
    
    
    