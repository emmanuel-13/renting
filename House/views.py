from datetime import datetime
from email import message
from django.urls import reverse_lazy, reverse

from customer.models import MailMessage, Subscribers
from .forms import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
from .models import *
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render, redirect
from django.http import HttpResponse
import calendar
from calendar import HTMLCalendar
import csv
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.paginator import Paginator
import pandas as pd
from payment.models import Payment, BookItem
from django.core.mail import send_mass_mail, send_mail, BadHeaderError
from django.template.loader import render_to_string
from django_pandas.io import read_frame

@staff_member_required
@login_required
def dashboard(request):
    if request.user.is_superuser:
        apartment = Estate.objects.all().count()
        user_name = User.objects.filter(is_active=True, is_staff=True).count()
        payment = BookItem.objects.filter(status=True).count()
        pending = Payment.objects.filter(status=False).count()
        booking = BookItem.objects.order_by('book_date')[:5]
        mail = MailMessage.objects.order_by('date_created')[:5]
        room_available = Room.objects.filter(active=False).count()
        room_occupied = Room.objects.filter(active=True).count()
            
        
        city = []
        estate_name = []
        estate = Estate.objects.all()[:2]
        for estate in estate:
            estate_name.append(estate.estate_name)
            city.append(estate.id)
        
        room_name = []
        price = []
        room = BookItem.objects.filter(status=True)[:5]
        
        for rooms in room:
            room_name.append(rooms.room.unique_room_id)
            price.append(int(rooms.price))    
        
        context = {
            'user_name': user_name, 'estate': apartment, 'room_name': room_name, 
            'price': price, 'city': city, 'estate_name': estate_name, 'payment': payment,
            'pending': pending, 'booking': booking, 'mail': mail, 
            "room_available": room_available, "room_occupied":room_occupied
        }
        return render(request, 'Dashboard/dashboard.html', context)
    
    else:
        apartment = Estate.objects.all().count()
        user_name = User.objects.filter(is_active=True, is_staff=False).count()
        payment = BookItem.objects.filter(status=True).count()
        pending = Payment.objects.filter(status=False).count()
        booking = BookItem.objects.filter(status=True)
        room_available = Room.objects.filter(active=False).count()
        room_occupied = Room.objects.filter(active=True).count()
        mail = MailMessage.objects.order_by('date_created')[:5]
    
        city = []
        estate_name = []
        estate = Estate.objects.all()[:2]
        for estate in estate:
            estate_name.append(estate.estate_name)
            city.append(estate.id)
        
        room_name = []
        price = []
        room = BookItem.objects.filter(status=True)[:5]
        
        for rooms in room:
            room_name.append(rooms.room.unique_room_id)
            price.append(int(rooms.price))    
        
        context = {
            'user_name': user_name, 'estate': apartment, 'room_name': room_name, 
            'price': price, 'city': city, 'estate_name': estate_name, 'payment': payment,
            'pending': pending, 'booking': booking, 'room_available': room_available, "room_occupied":room_occupied, "mail": mail
        }
        return render(request, 'Dashboard/dashboard.html', context)


class EstateCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Estate
    template_name = 'rooms/apartment.html'
    success_message = "estate %(estate)'s created successfully"
    success_url = None
    form_class = EstateForm
    object = None

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        blocks = BlockFormset()
        return self.render_to_response(self.get_context_data(form=form, blocks=blocks))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        blocks = BlockFormset(self.request.POST, instance=form.instance)
        

        if form.is_valid() and blocks.is_valid():
            return self.form_valid(form, blocks)
        else:
            return self.form_invalid(form, blocks)

    def form_valid(self, form, blocks):
        form.instance.owner = self.request.user
        self.object = form.save(commit=False)
        self.object.save()
        
        for files in self.request.FILES.getlist('image'):
            EstateImage.objects.create(
                estate=self.object,
                images=files
            )
            
        property_detail = self.request.POST.get('property_detail')
        additional_detail = self.request.POST.get('additional_detail')
        feature = self.request.POST.get('feature')
        video = self.request.FILES.get('video')
        
        Estate_property.objects.create(
            estate=self.object, property_detail=property_detail, additional_details=additional_detail,
            feature=feature, property_video=video
        )
        

        # saving Block Instances
        block = blocks.save(commit=False)
        for aq in block:
            aq.save()

        messages.success(self.request, f'apartment created successfully')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, blocks):
        return self.render_to_response(self.get_context_data(form=form, blocks=blocks))

    def get_success_url(self):
        return reverse_lazy('estate_list')
    


# class EstateUpdate(UpdateView):
#     model = Estate
#     template_name = 'rooms/apartment.html'
#     form_class = EstateForm
#     object = None

#     def get_object(self, queryset=None):
#         self.object = super(EstateUpdate, self).get_object()
#         return self.object

#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         block = BlockFormset(instance=self.object)
#         return self.render_to_response(
#                   self.get_context_data(form=EstateForm(instance=self.object), blocks=block)
#                   )

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form = EstateForm(data=self.request.POST, instance=self.object)
#         block = BlockFormset(data=self.request.POST, instance=self.object)
        
#         if form.is_valid() and block.is_valid():
#             return self.form_valid(form, block)
#         else:
#             return self.form_invalid(form, block)

#     def form_valid(self, form, block):
#         self.object = form.save()
        
#         blocks = block.save(commit=False)
#         for aq in self.objects.blocks_set.all():
#             print(aq.id)
#             aq.save()

#         # messages.success(self.request, f'apartment updated successfully')
        
        
#     def get_success_url(self):
#         return reverse_lazy('estate_list')
    

#     def form_invalid(self, form, block):
#         print('invalid form')
#         print(block.errors)
#         return self.render_to_response(self.get_context_data(form=form, blocks=block))
        
        
    # def get_success_url(self):
    #     return reverse_lazy('estate_list')
    
    

@staff_member_required
@login_required
def EstateDeleteView(request, pk):
    if request.user.is_superuser:
        estate = get_object_or_404(Estate, pk=pk)
        block = Block.objects.filter(estate_names=estate).first()
        apartment = Apartment.objects.filter(block=block, estate_name=estate).all()

        if request.method == "POST":
            if Block.objects.filter(estate_names=estate).exists():
                Block.objects.filter(estate_names=estate).delete()
                estate.delete()
                apartment.delete()
                if Room.objects.filter(blocks=block).exists():
                    room = Room.objects.filter(apartment_name_rooms=estate).all()
                    room.delete()
                else:
                    pass
            else:
                estate.delete()

            messages.success(request, 'Estate has been deleted successfully')
            return redirect('estate_edit')

        context = {
            'estate': estate
        }
        return render(request, 'rooms/apartment_delete.html', context)
    else:
        estate = get_object_or_404(Estate, pk=pk, owner=request.user)
        block = Block.objects.filter(estate_names=estate).first()
        apartment = Apartment.objects.filter(block=block, estate_name=estate, owner=request.user).all()

        if request.method == "POST":
            if Block.objects.filter(estate_names=estate).exists():
                Block.objects.filter(estate_names=estate).delete()
                estate.delete()
                apartment.delete()
                if Room.objects.filter(blocks=block).exists():
                    room = Room.objects.filter(apartment_name_rooms=estate, owner_room=request.user).all()
                    room.delete()
                else:
                    pass
            else:
                estate.delete()
            

            messages.success(request, 'apartment is deleted successfully')
            return redirect('estate_edit')

        context = {
            'estate': estate
        }
        return render(request, 'rooms/apartment_delete.html', context)
        


class EstateListView(LoginRequiredMixin, ListView):
    model = Estate
    template_name = 'rooms/apartment_list.html'
    context_object_name = 'estate'
    ordering = ("-estate_name",)
    
    def get_queryset(self):
        if self.request.user.is_staff and self.request.user.is_superuser:
            return Estate.objects.all()
        else:
            owner = get_object_or_404(User, username=self.request.user.username)
            return Estate.objects.filter(owner=owner)
    


class EstateEdit(LoginRequiredMixin, ListView):
    model = Estate
    template_name = 'rooms/apartment_edit.html'
    context_object_name = 'estate'
    
    def get_queryset(self):
        if self.request.user.is_staff and self.request.user.is_superuser:
            return Estate.objects.all()
        else:
            owner = get_object_or_404(User, username=self.request.user.username)
            return Estate.objects.filter(owner=owner)
    


@staff_member_required
@login_required(login_url='login')
def estate_detail(request, estate_name):
    estate = get_object_or_404(Estate, estate_name=estate_name)
    block = Block.objects.filter(estate_names=estate).all()
    # apartment = Apartment.objects.get(block=block, estate_name=estate).count()

    context = {
        'estate': estate, 'block': block
    }
    return render(request, "rooms/apartment_detail.html", context)


@staff_member_required
@login_required(login_url='login')
def block_details(request, estate_id, pk):
    blocks = get_object_or_404(Block, estate_names_id=estate_id, pk=pk)
    estate = Estate.objects.filter(estate_name=blocks.estate_names).first()
    apartment = Apartment.objects.filter(estate_name=estate, block=blocks.block_no).all()

    apartments = Apartment.objects.filter(block=blocks.block_no, estate_name=estate)
    print(apartments)

    room = Room.objects.all()
    print(room)
    appended = []
    for apart in apartments:
        for rooms in room:
            if apart.flat_id in rooms.flat_id_rooms:
                appended.append(apart.flat_id)

    print(appended)
    context = {
        'apartment': apartment, 'blocks': blocks, "estate": estate, 'room': appended
    }

    return render(request, 'rooms/block_details.html', context)

@staff_member_required
@login_required(login_url='login')
def apartment_room_details(request, flat_id):
    apartment = get_object_or_404(Apartment, flat_id=flat_id)
    estate = Estate.objects.get(estate_name=apartment.estate_name)
    block = Block.objects.all().filter(estate_names=estate)
    # print(apartment.block)

    b = []
    for block in block:
        if apartment.block in block.block_no:
            b.append(block.pk)
    print(b[0])
    room = Room.objects.filter(apartment_name_rooms=apartment.estate_name).all()
    # print(apartment.flat_id)

    new_room = []
    for rooms in room:
        if apartment.flat_id in rooms.flat_id_rooms:
            new_room.append(rooms)

    context = {
        'room': new_room, "apartment": apartment, 'estate': estate, 'b': b[0]
    }

    return render(request, 'rooms/apartment_rooms_detail.html', context)


@staff_member_required
@login_required(login_url='login')
def apartment_update(request, flat_id):
    apartment = get_object_or_404(Apartment, flat_id=flat_id)
    form = ApartmentForm(instance=apartment)

    estate = Estate.objects.filter(estate_name=apartment.estate_name).first()
    block = Block.objects.all().filter(estate_names=estate)
    # print(apartment.block)

    b = []
    for block in block:
        if apartment.block in block.block_no:
            b.append(block.pk)
    print(b[0])
    room = Room.objects.filter(apartment_name_rooms=apartment.estate_name).all()
    # print(apartment.flat_id)

    new_room = []
    for rooms in room:
        if apartment.flat_id in rooms.flat_id_rooms:
            new_room.append(rooms)

    if request.method == "POST":
        form = ApartmentForm(request.POST, request.FILES, instance=apartment)

        if form.is_valid():
            form.save()

            messages.success(request, f'apartment {apartment.flat_id} updated successfully')
            return redirect(reverse('block_details', kwargs={'estate_id': estate.id, 'pk': b[0]}))

    context = {
        'form': form, 'apartment': apartment, 'estate': estate, 'b': b[0]
    }

    return render(request, 'rooms/apartment_update.html', context)


@staff_member_required
@login_required(login_url='login')
def estate_list(request):
    if request.user.is_superuser and request.user.is_staff:
        estate_filter = EstateFilter(request.GET, queryset=Estate.objects.all())

        p = Paginator(estate_filter.qs, 5)
        page = request.GET.get('page')
        estates = p.get_page(page)
        context = {
            'filter': estate_filter, 'estates': estates
        }
        return render(request, 'rooms/estate_apartment_list.html', context)
    else:
        estate_filter = EstateFilter(request.GET, queryset=Estate.objects.filter(owner=request.user))

        p = Paginator(estate_filter.qs, 5)
        page = request.GET.get('page')
        estates = p.get_page(page)
        context = {
            'filter': estate_filter, 'estates': estates
        }
        return render(request, 'rooms/estate_apartment_list.html', context)


@staff_member_required
@login_required(login_url='login')
def apartment_list(request, estate_name):
    estate = get_object_or_404(Estate, estate_name=estate_name)
    apartment = Apartment.objects.filter(estate_name=estate)

    if not apartment:
        messages.info(request, f'no apartment found in this estate {estate}')
        return redirect('estate_listing')
    else:
        apartment_filter = ApartmentFilter(request.GET, queryset=apartment)
    
        p = Paginator(apartment_filter.qs, 5)
        page = request.GET.get('page')
        apartments = p.get_page(page)

        context = {
            "apartments": apartments, "myfilter": apartment_filter, 'estate': estate, 'apartment': apartment
        }

        return render(request, 'rooms/estate_list.html', context)

@staff_member_required
@login_required(login_url='login')
def estate_csv(request):
    response = HttpResponse(content_type="txt/csv")
    response['Content-Disposition'] = 'attachment; filename=estate.csv'

    # creating a csv writer
    writer = csv.writer(response)

    apartment = Estate.objects.all()

    # adding columns
    writer.writerow(['Estate Name', 'City', 'Location', 'Block'])

    for apartment in apartment:
        writer.writerow([apartment.estate_name, apartment.city, apartment.location, apartment.block_set.count()])

    return response

@staff_member_required
@login_required(login_url='login')
def apartment_csv(request, estate_name):
    response = HttpResponse(content_type="txt/csv")
    response['Content-Disposition'] = 'attachment; filename=apartment.csv'

    # creating a csv writer
    writer = csv.writer(response)

    estate = get_object_or_404(Estate, estate_name=estate_name)
    apartment = Apartment.objects.filter(estate_name=estate.estate_name)

    # adding columns
    writer.writerow(['Block', 'Apartment_Type', 'Flat_id'])

    for apartment in apartment:
        writer.writerow([apartment.block, apartment.flat_types, apartment.flat_id, apartment.bedroom_type, apartment.apartment_type])

    return response


@staff_member_required
@login_required(login_url='login')
def room_csv(request):
    response = HttpResponse(content_type="txt/csv")
    response['Content-Disposition'] = 'attachment; filename=Room.csv'

    # creating a csv writer
    writer = csv.writer(response)

    room = Room.objects.all()

    # adding columns
    writer.writerow(['Estate', 'Blocks', 'Room ID', 'Room Type', 'Apartment Type','Occupied'])

    for apartment in room:
        writer.writerow([apartment.apartment_name_rooms, apartment.blocks, apartment.unique_room_id,  apartment.room_types, apartment.exclusive_room, apartment.occupied])

    return response


@staff_member_required
@login_required(login_url='login')
def apartment_test(request, apartment_pk):
    apartment = get_object_or_404(Apartment, pk=apartment_pk)
    estate = Estate.objects.get(estate_name=apartment.estate_name)
    form = ApartmentForm(instance=apartment)

    if request.method == "POST":
        form = ApartmentForm(request.POST, request.FILES, instance=apartment)

        if form.is_valid():
            form.save()

            messages.success(request, f'room {apartment.flat_id} updated successfully')
            return redirect(reverse('apartment_list', kwargs={'estate_name': estate.estate_name}))

    context = {
        'form': form, 'apartment': apartment, 'estate': estate
    }
    return render(request, 'rooms/apartment_test.html', context)


@staff_member_required
@login_required(login_url='login')
def apartment_room_test(request, flat_id):
    apartment = get_object_or_404(Apartment, flat_id=flat_id)
    estate = Estate.objects.get(estate_name=apartment.estate_name)

    room = Room.objects.filter(apartment_name_rooms=apartment.estate_name).all()
    # print(apartment.flat_id)

    new_room = []
    for rooms in room:
        if apartment.flat_id in rooms.flat_id_rooms:
            new_room.append(rooms)

    context = {
        'room': new_room, "apartment": apartment, 'estate': estate
    }

    return render(request, 'rooms/apartment_room_test.html', context)


@staff_member_required
@login_required(login_url='login')
def room_update(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)

    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES, instance=room)

        if form.is_valid():
            new = form.save(commit=False)
            new.save()
            
            for files in request.FILES.getlist('image'):
                RoomImages.objects.create(
                room=new,
                images=files
            )

            messages.success(request, f'room {room.unique_room_id} updated successfully')
            return redirect(reverse('apartment_room_test', kwargs={'flat_id': room.flat_id_rooms}))

    context = {
        'form': form, 'room': room
    }
    return render(request, 'rooms/room_create_update.html', context)


@staff_member_required
@login_required(login_url='login')
def room_update2(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)

    form = RoomForm2(instance=room)

    if request.method == "POST":
        form = RoomForm2(request.POST, request.FILES, instance=room)
        

        if form.is_valid():
            new = form.save(commit=False)
            new.save()
            
            for files in request.FILES.getlist('image'):
                RoomImages.objects.create(
                room=new,
                images=files
            )

            messages.success(request, f'room {room.unique_room_id} updated successfully')
            return redirect(reverse('apartment_room_test', kwargs={'flat_id': room.flat_id_rooms}))

    context = {
        'form': form, 'room': room
    }
    return render(request, 'rooms/room_create_update.html', context)


@staff_member_required
@login_required(login_url='login')
def room_detail(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)

    context = {
        "room": room
    }
    return render(request, 'rooms/room_detail.html', context)


@staff_member_required
@login_required(login_url='login')
def room_detail_main(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)

    context = {
        "room": room
    }
    return render(request, 'rooms/room_main_detail.html', context)


@staff_member_required
@login_required(login_url='login')
def room_list(request):
    if request.user.is_staff and request.user.is_superuser:
        room = Room.objects.all()
        myfilter = RoomFilter(request.GET, queryset=room)
        context = {
            'room': room, 'myfilter': myfilter
        }
        return render(request, 'rooms/room_list.html', context)
    else:
        room = Room.objects.all()
        myfilter = RoomFilterer(request.GET, queryset=room)
        context = {
            'room': room, 'myfilterer': myfilter
        }
        return render(request, 'rooms/room_list.html', context)


@staff_member_required
@login_required(login_url='login')
def room_update_2(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)

    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES, instance=room)

        if form.is_valid():
            new = form.save(commit=False)
            new.save()
            
            for files in request.FILES.getlist('image'):
                RoomImages.objects.create(
                room=new,
                images=files
            )

            messages.success(request, f'room {room.unique_room_id} updated successfully')
            return redirect("room_list")

    context = {
        'form': form, 'room': room
    }
    return render(request, 'rooms/room_update.html', context)


@staff_member_required
@login_required(login_url='login')
def room_updater(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)

    form = RoomForm2(instance=room)

    if request.method == "POST":
        form = RoomForm2(request.POST, request.FILES, instance=room)

        if form.is_valid():
            new = form.save(commit=False)
            new.save()
            
            for files in request.FILES.getlist('image'):
                RoomImages.objects.create(
                room=new,
                images=files
            )

            messages.success(request, f'room {room.unique_room_id} updated successfully')
            return redirect(reverse('apartment_room_test', kwargs={'flat_id': room.flat_id_rooms}))

    context = {
        'form': form, 'room': room
    }
    return render(request, 'rooms/room_update.html', context)


@staff_member_required
@login_required(login_url='login')
def room_update_per_shared(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)

    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES, instance=room)
        
        

        if form.is_valid():
            new = form.save(commit=False)
            new.save()
            
            for files in request.FILES.getlist('image'):
                RoomImages.objects.create(
                room=new,
                images=files
            )

            messages.success(request, f'room {room.unique_room_id} updated successfully')
            return redirect(reverse("room_det", kwargs={'flat_id': room.flat_id_rooms}))

    context = {
        'form': form, 'room': room
    }
    return render(request, 'rooms/room_update_block.html', context)


@staff_member_required
@login_required(login_url='login')
def room_updater_per_exclusive(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)

    form = RoomForm2(instance=room)

    if request.method == "POST":
        form = RoomForm2(request.POST, request.FILES, instance=room)

        if form.is_valid():
            new = form.save(commit=False)
            new.save()
            
            for files in request.FILES.getlist('image'):
                RoomImages.objects.create(
                room=new,
                images=files
            )

            messages.success(request, f'room {room.unique_room_id} updated successfully')
            return redirect(reverse("room_det", kwargs={'flat_id': room.flat_id_rooms}))

    context = {
        'form': form, 'room': room
    }
    return render(request, 'rooms/room_update_block.html', context)

@staff_member_required
@login_required(login_url='login')
def subscriber(request):
    subscriber = Subscribers.objects.all()
    return render(request, 'subsciber.html', {'subscriber': subscriber})



from django.db.models import Case, When

@login_required(login_url='login')
def user_history_for_estate(request):
    if request.method == "POST":
        user = request.user
        estate_name = request.POST['estate_name']
        
        history_estate = EstateHistory(user=user, estate_name=estate_name)
        history_estate.save()
        return redirect(reverse("apartment_detail", kwargs={"estate_name": estate_name}))
    
    hist_estate = EstateHistory.objects.filter(user=request.user)
    
    ids = []
    for i in hist_estate:
        ids.append(i.estate_name)
        
    preversed = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    estate = Estate.objects.filter(id__in=ids).order_by(preversed)
        
    return render(request, 'user_history.html', {'estate': estate})

@login_required(login_url='login')
def clear_estate_history(request):
    history = EstateHistory.objects.filter(user=request.user)
    if history:
        for history in history:
            history.delete()
    
    return redirect('history_estate')
    

@staff_member_required
@login_required(login_url='login')  
def list_messages(request):
    new_messgaes = DevelopmentMessage.objects.all().order_by("-date_created")[:5]
    return render(request, 'development/new_messages.html', {'new_messages': new_messgaes, 'admin': admin_messages })
    
    
@staff_member_required
@login_required(login_url='login')
def admin_messages(request):
    admin_messages = AdminMessage.objects.all().order_by('-date_created')[:5]
    return render(request, 'development/admin_messages.html', {'admin_messages': admin_messages })
    
    
@staff_member_required
@login_required(login_url='login')
def create_message(request):
    create_form = DevelopmentForm()
    subscriber = User.objects.all()
    
    df = read_frame(subscriber, fieldnames=['email'])
    new_mail = df['email'].values.tolist()
    print(new_mail)
    
    if request.method == "POST":
        create_form = DevelopmentForm(request.POST)
        
        if create_form.is_valid():
            create_form.save()
            title = create_form.cleaned_data.get('title')
            description = create_form.cleaned_data.get('description')
            
            messages.info(request, 'form saved successfully')
            send_mail(subject=title, message=description, from_email="emmysoln@gmail.com", recipient_list=new_mail)
            return redirect('list_messages')
        else:
            response = "invalid"
            return JsonResponse(response)
            
    return render(request, 'development/create_update.html', {'create_form': create_form })

@staff_member_required
@login_required(login_url='login')
def admin_create_message(request):
    create_form = AdminForm()
    subscriber = User.objects.all()
    df = read_frame(subscriber, fieldnames=['email'])
    new_mail = df['email'].values.tolist()
    print(new_mail)
    
    if request.method == "POST":
        create_form = AdminForm(request.POST)
        
        if create_form.is_valid():
            create_form.instance.user = request.user
            new_object = create_form.save(commit=False)
            new_object.save()
            
            title = create_form.cleaned_data.get('title')
            description = create_form.cleaned_data.get('description')
            
            subject=title
            email_template_name = "textfile/admin_messages_create.html"
            c = {
            "email": request.user.email,
            "username": request.user.username,
            "title": title,
            'description': description,
            'site_name': 'rent4Less.com.ng',
            'protocol': 'http',
            }
            email = render_to_string(email_template_name, c)
            try:
                send_mail(subject, email, 'rent4less.mgt@gmail.com' , new_mail, fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            
            messages.info(request, 'form saved successfully')
            return redirect('admin_messages')
        else:
            response = "invalid"
            return JsonResponse(response)
            
    return render(request, 'development/admin_create_update.html', {'admin_create_form': create_form })


@staff_member_required
@login_required(login_url='login')
def update_message(request, pk):
    dev = get_object_or_404(DevelopmentMessage, pk=pk)
    
    subscriber = User.objects.all()
    df = read_frame(subscriber, fieldnames=['email'])
    new_mail = df['email'].values.tolist()
    print(new_mail)
    
    if request.method == "POST":
        create_form = DevelopmentForm(request.POST, instance=dev)
            
        if create_form.is_valid():
            create_form.save()
            title = create_form.cleaned_data.get('title')
            description = create_form.cleaned_data.get('description')
            
            messages.info(request, f'{dev} updated successfully')
            send_mail(subject=title, message=description, from_email="emmysoln@gmail.com", recipient_list=new_mail)
            return redirect('list_messages')
        else:
            response = "invalid"
            return JsonResponse(response)
    else:
        create_form = DevelopmentForm(instance=dev)
        
    return render(request, 'development/create_update.html', {'update_form': create_form , 'dev': dev})


def check_profile_owner(request, owner):
    if request.user != owner:
        messages.info(request, 'you can\'t update another admin message' )
        raise HttpResponseRedirect('admin_messages')

@staff_member_required
@login_required(login_url='login')
def admin_update_message(request, id):
    admining = get_object_or_404(AdminMessage, id=id)
    
    subscriber = User.objects.filter(is_active=True, is_staff=True, is_superuser=True)
    df = read_frame(subscriber, fieldnames=['email'])
    new_mail = df['email'].values.tolist()
    print(new_mail)
    
    check_profile_owner(request, admining.user)
    if request.method == "POST":
        create_form = AdminForm(request.POST, instance=admining)
            
        if create_form.is_valid():
            create_form.instance.user = request.user
            new_object = create_form.save(commit=False)
            new_object.save()
            
            title = create_form.cleaned_data.get('title')
            description = create_form.cleaned_data.get('description')
            
            messages.info(request, f'{admining} updated successfully')
            send_mail(subject=title, message=description, from_email="emmysoln@gmail.com", recipient_list=new_mail)
            return redirect('admin_messages')
        else:
            response = "invalid"
            return JsonResponse(response)
    else:
        create_form = AdminForm(instance=admining)
        
    return render(request, 'development/admin_create_update.html', {'admin_update_form': create_form , 'dev': admining})


@staff_member_required
@login_required(login_url='login')
def admin_delete_message(request, id):
    admin = AdminMessage.objects.get(id=id)
    admin.delete()
    return redirect('admin_messages')


@staff_member_required
@login_required(login_url='login')
def delete_message(request, pk):
    dev = get_object_or_404(DevelopmentMessage, pk=pk)
    dev.delete()
    return redirect('list_messages')
            

