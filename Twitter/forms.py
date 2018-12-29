from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from Twitter.models import Tweet, Profile


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True,
                             widget=forms.widgets.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={'placeholder': 'Name', 'class': 'form-control'}))
    username = forms.CharField(
        widget=forms.widgets.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    password1 = forms.CharField(
        widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))
    password2 = forms.CharField(
        widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password Confirmation', 'class': 'form-control'}))

    class Meta:
        fields = ['email', 'username', 'first_name', 'password1', 'password2']
        model = User

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        confirm_password = cleaned_data.get('password2')
        password = cleaned_data.get('password1')
        if not password == confirm_password:
            raise forms.ValidationError('Password does not match.')


class SigninForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.widgets.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))


class TweetForm(forms.ModelForm):
    title = forms.CharField(required=True,
                            widget=forms.widgets.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control'}))
    text = forms.CharField(required=True,
                           widget=forms.widgets.Textarea(
                               attrs={'placeholder': "What's Happening?", 'class': 'form-control', 'rows': "1",
                                      'cols': "40", 'onfocus': "this.rows=3;", 'onblur': "this.rows=1;"}))

    class Meta:
        model = Tweet
        exclude = ('user', 'created_at')


class EditProfileForm(forms.ModelForm):
    bio = forms.CharField(required=False,
                          widget=forms.widgets.Textarea(attrs={'placeholder': 'Bio', 'class': 'form-control'}))
    birthday = forms.CharField(required=False, widget=forms.widgets.DateInput(
        attrs={'placeholder': 'year-month-day', 'class': 'form-control'}))
    image = forms.ImageField(required=False)

    class Meta:
        model = Profile
        exclude = ('user', 'joined')
