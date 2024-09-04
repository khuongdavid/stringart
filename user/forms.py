from django import forms
from .models import User
from django.core.validators import RegexValidator

class CreateUserForm(forms.ModelForm): 

    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control m-2', 
                'placeholder': 'Tên đăng nhập'}))
    firstname = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control m-2', 
                'placeholder': 'Họ'}))
    lastname = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control m-2', 
                'placeholder': 'Tên'}))
    email = forms.EmailField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control m-2', 
                'placeholder': 'Email'}))
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class': 'form-control m-2', 
                'placeholder': 'Mật khẩu', 'type': 'password'}))
    confirmpassword = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class': 'form-control m-2',
                'placeholder': 'Nhập lại mật khẩu', 'type': 'password'}))
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmpassword = cleaned_data.get('confirmpassword')

        if password and confirmpassword:
            if password != confirmpassword:
                self.add_error('confirmpassword', 'Mật khẩu và mật khẩu xác nhận không khớp.')
        return cleaned_data

    class Meta:
        model = User
        fields = ['username', 'firstname', 'lastname', 'email', 'password']
    

class LoginForm(forms.Form):

    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control m-2', 
                'placeholder': 'Tên đăng nhập'}))
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class': 'form-control m-2', 
                'placeholder': 'Mật khẩu', 'type': 'password'}))
    class Meta:
        model = User
        fields = ['username', 'password']


class EditUserForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Số điện thoại không hợp lệ. Số điện thoại phải từ 9 đến 15 chữ số."
    )
    oldpassword = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={
        'class': 'form-control m-2',
        'placeholder': 'Nhập mật khẩu cũ',
        'type': 'password'
    }))
    newpassword = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={
        'class': 'form-control m-2',
        'placeholder': 'Nhập mật khẩu mới',
        'type': 'password'
    }), required=False)
    confirmpassword = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={
        'class': 'form-control m-2',
        'placeholder': 'Nhập lại mật khẩu mới',
        'type': 'password'
    }), required=False)
    image = forms.FileField(max_length=255, widget=forms.FileInput(attrs={
        'class': 'form-control btn btn-primary mgt-3',
        'accept': 'image/*'
    }), required=False)
    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'email', 'phone']
        widgets = {
            'firstname': forms.TextInput(attrs={
                'class': 'form-control m-2',
                'placeholder': 'Họ'
            }),
            'lastname': forms.TextInput(attrs={
                'class': 'form-control m-2',
                'placeholder': 'Tên'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control m-2',
                'placeholder': 'Email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control m-2',
                'placeholder': 'Số điện thoại'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['newpassword'].required = False
        self.fields['confirmpassword'].required = False
        self.fields['image'].required = False
        self.fields['phone'].required = False

        
            

def clean(self):
    cleaned_data = super().clean()
    newpassword = cleaned_data.get("newpassword")
    confirmpassword = cleaned_data.get("confirmpassword")
    phone = cleaned_data.get("phone")
    
    phone_regex = self.phone_regex
    if not phone_regex(phone):
        self.add_error('phone', message)
        
        
    if newpassword != confirmpassword:
        self.add_error('confirmpassword', "Mật khẩu không khớp")

