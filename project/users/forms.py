from django import forms
from django.contrib.auth.hashers import check_password
from .models import User
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, SetPasswordForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from .choice import *


# 로그인 폼
class LoginForm(forms.Form):
    user_id = forms.CharField(
        widget=forms.TextInput(
        attrs={'class': 'form-control',}), 
        error_messages={
            'required': '아이디을 입력해주세요.'
        },
        max_length=32,
        label='아이디'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
        attrs={'class': 'form-control',}), 
        error_messages={
            'required': '비밀번호를 입력해주세요.'
        },
        label='비밀번호'
    )

    def clean(self):
        cleaned_data = super().clean()
        user_id = cleaned_data.get('user_id')
        password = cleaned_data.get('password')

        if user_id and password:
            try:
               user = User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                self.add_error('user_id', '아이디가 존재하지 않습니다.')
                return
            
            if not check_password(password, user.password):
                self.add_error('password', '비밀번호가 틀렸습니다.')


# 회원가입 폼
class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['user_id'].label = '아이디'
        self.fields['user_id'].widget.attrs.update({
            'class': 'form-control',
            'autofocus': False
        })
        self.fields['password1'].label = '비밀번호'
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['password2'].label = '비밀번호 확인'
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['email'].label = '이메일'
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['name'].label = '이름'
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['phone'].label = '핸드폰번호'
        self.fields['phone'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['location'].label = '거주지'
        self.fields['location'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['sns'].label = 'SNS아이디'
        self.fields['sns'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['genre'].label = '분야'
        self.fields['genre'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['position'].label = '세부분야'
        self.fields['position'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['profile_image'].label = '프로필사진'
        self.fields['profile_image'].widget.attrs.update({
            'class': 'form-control'
        })

    class Meta:
        model = User
        fields = ['user_id', 'password1', 'password2', 'email', 'name', 'phone', 'location', 'sns', 'genre', 'position', 'profile_image']

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.level = '2'
        user.save()

        return user