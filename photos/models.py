from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from tinymce.models import HTMLField 
from django.dispatch import receiver

# Create your models here.


class Profile(models.Model):
    pro_picture = models.ImageField(upload_to = 'profile-pics', null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_bio = HTMLField()


    def __str__(self):
        return self.user.username


class Image (models.Model):
    image_name = models.CharField(max_length =60, null=True)
    image_caption = models.CharField(max_length =200)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image_likes = models.ManyToManyField(User, related_name='likes', blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    post_image = models.ImageField(upload_to = 'my-photos/', null=True)

    def __str__(self):
        return self.image_caption

 

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()

    @classmethod
    def search_by_name(cls,search_term):
        photos = cls.objects.filter(name__icontains=search_term)
        return photos
    
    @classmethod
    def posted_pics(cls):
        photos = cls.objects.all()
        return photos
    
class WelcomeMessageRecipient(models.Model):
    name = models.CharField(max_length = 30)
    email = models.EmailField()

class Comment(models.Model):
    comment = models.TextField(blank=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
   

    def __str__(self):
        return self.comment

    @classmethod
    def get_comments(cls, image_id):
        comments = cls.objects.filter(image=image_id)
        return comments

