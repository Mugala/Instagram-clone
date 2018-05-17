from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect 
import datetime as dt
from .models import Image,WelcomeMessageRecipient,Comment,Profile
from .forms import WelcomeMessageForm,NewCommentForm,NewImageForm,EditUserForm,EditProfile
from .email import send_welcome_email
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
import cloudinary
import cloudinary.uploader
import cloudinary.api

def welcome(request):
    return render (request, "welcome.html")

@login_required(login_url='/accounts/login/')
def home(request):
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


def user_profile(request):  
    current_user = request.user
    if request.method =='POST':
        form = EditProfile(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()

            return redirect("home")
    else:
        form = EditProfile()
    return render (request, 'all-photos/edit_profile.html',{"form":form})



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
@login_required(login_url='/accounts/login/')    
def image(request,image_id):
    try:
        image = Image.objects.get(id = image_id)
    except DoesNotExist:
        raise Http404()
    return render(request,"all-photos/images.html", {"image":image})

@login_required(login_url = '/accounts/login/')
def new_image(request):
    current_user = request.user
    if request.method =='POST':
        form = NewImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = current_user
            image.save()
    else:
        form = NewImageForm()
    return render (request, 'all-photos/new_image.html', {"form":form})

def like_image(request, image_id):
    image = Image.objects.get(pk=image_id)
    is_liked = False
    if image.likes.filter(id=request.user.id).exists():
            image.likes.remove(request.user)
            is_liked = False

    else:
        image.likes.add(request.user)
        is_liked = True
    HttpResponseRedirect(request.META.get('HTTP_REFERER'))
 
@login_required(login_url='/accounts/login/')
def post_comment(request, image_id):
    current_user = request.user
    photo = get_object_or_404(Image, id=image_id)
   
    if request.method == 'POST':
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.image = photo
            comment.user = current_user
            comment.save()
            return redirect("home")
            
    else:
        comment_form = NewCommentForm()

    # comments = Comment.get_comments(image=current_user)
    # context = {"title": title, "photo": photo, "comments": comments, "comment_form": comment_form, "current_user": current_user}
    return render(request, 'all-photos/comments.html', {"form":comment_form, "image_id": image_id})

@login_required(login_url='/accounts/login/')   
def upload_photo(request):
    current_user = request.user
    current_profile = current_user.profile
    if request.method == 'POST':
        uploads_form = NewImageForm(request.POST, request.FILES)
        if uploads_form.is_valid():
            post = uploads_form.save(commit=False)
            post.user = current_user
            post.profile = current_profile
            post.save()
            print(post)
            return redirect("home")
    else:
        uploads_form = NewImageForm()
    return render(request, 'all-photos/new_image.html', {"uploads_form": uploads_form, "current_user": current_user})
