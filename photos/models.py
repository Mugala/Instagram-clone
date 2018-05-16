from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from tinymce.models import HTMLField 

# Create your models here.


class Profile(models.Model):
    pro_picture = models.ImageField(upload_to = 'profile-pics', null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_bio = HTMLField()

class Comment(models.Model):
    user_comment = HTMLField()

class Image (models.Model):
    image_name = models.CharField(max_length =60, null=True)
    image_caption = models.CharField(max_length =200)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    image_comment = models.ManyToManyField(Comment)
    image_likes = models.ManyToManyField(User, related_name='likes', blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    post_image = models.ImageField(upload_to = 'my-photos/', null=True)

    def __str__(self):
        return self.image_caption

    class Meta:
        ordering = ['pub_date']

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
        today = dt.date.today()
        photos = cls.objects.filter(pub_date__date = today)
        return photos
    
class WelcomeMessageRecipient(models.Model):
    name = models.CharField(max_length = 30)
    email = models.EmailField()



