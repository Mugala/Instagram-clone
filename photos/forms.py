from django import forms
from .models import Comment,Image


class WelcomeMessageForm(forms.Form):
    your_name = forms.CharField(label='First Name', max_length=30)
    email = forms.EmailField(label='Email')
    
class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['image', 'pub_date']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
    
class NewImageForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['User','pub_date']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

        