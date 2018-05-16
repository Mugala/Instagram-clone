from django.shortcuts import render, redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect 
import datetime as dt
from .models import Image,WelcomeMessageRecipient
from .forms import WelcomeMessageForm
from .email import send_welcome_email
# Create your views here.

def welcome(request):
    return render (request, "welcome.html")

def home(request):
    date = dt.date.today
    pics = Image.posted_pics()

    if request.method =='POST':
        form = WelcomeMessageForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']

            recipient = WelcomeMessageRecipient(name=name,email=email)
            recipient.save()
            send_welcome_email(name,email)

            HttpResponseRedirect('home')
    else:
        form = WelcomeMessageForm()

    return render (request, 'all-photos/home.html',{"pics":pics,"letterForm":form})

def search_results(request):

    if 'image' in request.GET and request.GET["image"]:
        search_term = request.GET.get("image")
        searched_images_by_category = Image.search_by_category(search_term)
        searched_images_by_location = Image.search_by_location(search_term)
        results = [*searched_images_by_category, *searched_images_by_location]
        message = f"{search_term}"

        return render(request, 'all-photos/search.html',{"message":message,"images": results})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all-photos/search.html',{"message":message})
    
def image(request,category_id):
    try:
        image = Image.objects.get(id = category_id)
    except DoesNotExist:
        raise Http404()
    return render(request,"all-photos/images.html", {"image":image})
