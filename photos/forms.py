from django import forms
from .models import Comment,Image,Profile,User


class WelcomeMessageForm(forms.Form):
    your_name = forms.CharField(label='First Name', max_length=30)
    email = forms.EmailField(label='Email')
    
class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
    
class NewImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['post_image', 'image_name', 'image_caption']
        exclude = ['profile, user, Likes, comments']

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class EditProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['pro_picture', 'profile_bio']
        exclude = ['user']


        