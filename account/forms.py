# -*- coding: UTF-8 -*-
from django import forms
from django.contrib.auth.models import User

# 使用者登入表單
class LoginForm(forms.Form):
        username = forms.CharField()
        password = forms.CharField(widget=forms.PasswordInput)

        def __init__(self, *args, **kwargs):
                super(LoginForm, self).__init__(*args, **kwargs)
                self.fields['username'].label = "帳號"
                self.fields['password'].label = "密碼"

class RegistrationForm(forms.ModelForm):
        error_messages = {
                'duplicate_username': ("此帳號已被使用")
        }

        username = forms.RegexField(
                label="User name", max_length=30, regex=r"^[\w.@+-]+$",
                error_messages={
                        'invalid': ("帳號名稱無效")
                }
        )

        password = forms.CharField(label='Password',widget=forms.PasswordInput)
        password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

        class Meta:
                model = User
                fields = ('username', 'first_name', 'last_name', 'email')

        def clean_password2(self):
                cd = self.cleaned_data
                if cd['password'] != cd['password2']:
                        raise forms.ValidationError('Passwords don\'t match.')
                return cd['password2']

        def __init__(self, *args, **kwargs):
                super(RegistrationForm, self).__init__(*args, **kwargs)
                self.fields['username'].label = "帳號"
                self.fields['first_name'].label = "真實姓名"
                self.fields['last_name'].label = "學校名稱"
                self.fields['email'].label = "電子郵件"
                self.fields['password'].label = "密碼"
                self.fields['password2'].label = "再次確認密碼"

        def clean_username(self):
                # Since User.username is unique, this check is redundant,
                # but it sets a nicer error message than the ORM. See #13147.
                username = self.cleaned_data["username"]
                if self.instance.username == username:
                        return username
                try:
                        User._default_manager.get(username=username)
                except User.DoesNotExist:
                        return username
                raise forms.ValidationError(
                        self.error_messages['duplicate_username'],
                        code='duplicate_username',
                )