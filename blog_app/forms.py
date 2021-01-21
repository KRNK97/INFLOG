from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ValidationError
from .models import Profile, Post


class RegistrationForm(UserCreationForm):

    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email.endswith(".com") and '@' in email:
            return email
        else:
            raise ValidationError("Email doesn't end with a .com")


class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']


# update username and email
class UserUpdateForm(forms.ModelForm):

    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


# update profile picture
class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']


class PostForm(forms.ModelForm):

    title = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "title of your post"}))

    content = forms.CharField(widget=forms.Textarea(
        attrs={"class": "form-control", "placeholder": "write something here . . ."}))

    class Meta:
        model = Post
        fields = ['title', 'content']
