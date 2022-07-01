from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from base.models import Comment
from django import forms


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254,
                             help_text='Enter a valid email address')

    # Nested class used to describe the relationship between the form
    # and the model it describes
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]


class PostForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = [
            'title',
            'message',
        ]

class ReplyForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = [
            'message',
        ]

