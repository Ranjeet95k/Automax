from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Listing
from .forms import ListingForm
from django.contrib import messages
from Users.forms import LocationForm
from .filters import ListingFilter

def main_view(request):
    return render(request,"views/main.html",{"name":"Automax"})

@login_required
def home_view(request):
    listings=Listing.objects.all()
    listing_filter=ListingFilter(request.GET,queryset=listings)
    context={
        'listings':listings,
        "listing_filter":listing_filter,
    }
    return render(request, 'views/home.html',context)

@login_required
def list_view(request):
    if request.method=="POST":
        try:
            listing_form=ListingForm(request.POST, request.FILES)
            location_form=LocationForm(request.POST,)
            if listing_form.is_valid() and LocationForm.is_valid():
                listing=listing_form.save(commit=False)
                listing_location=location_form.save()
                listing.seller=request.user.profile
                listing.location=listing_location
                listing.save()
                messages.info(request, f'{listing.model} Listing Posted Successfully')
                return redirect('home')
            else:
                raise Exception()
        except Exception as e:
            print(e)
            messages.error('An error occured')
    elif request.method=="GET":
        listing_form=ListingForm()
        location_form=LocationForm()
    return render(request,'views/list.html',{'listing_form':listing_form,'location_form':location_form})


@login_required
def listing_view(request,id):
    try:
        listing=Listing.objects.get(id=id)
        if listing is None:
            raise Exception
        return render(request,'views/listing.html',{'listing':listing, })
    except Exception as e:
        messages.error(request,f' Invalid UID {id} was provided for listing')
        return redirect('home')
    return render(request,'views/listing.html',{})
