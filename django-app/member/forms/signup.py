from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput
    )
    nickname = forms.CharField(
        widget=forms.TextInput,

    )
    password1 = forms.CharField(
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'Username already exist'
            )
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1!= password2:
            raise forms.ValidationError(
                'password wrong'
            )
        return password2

    def create_user(self):
        username = self.cleaned_data.data['username']
        password = self.cleaned_data.data['password2']

        return User.objects.create_user(
            username=username,
            password=password
        )

    def create_user(self):
        nickname = self.cleaned_data['nickname']
        password = self.cleaned_data['password2']
        username = self.cleaned_data['username']
        if nickname and User.objects.filter(username=nickname).exists():
            raise forms.ValidationError(
                'Nickname already exist'
            )
        return User.objects.create_user(
            username=username,
            password=password,
            nickname=nickname,
        )