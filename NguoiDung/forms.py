from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,AuthenticationForm
from django.contrib.auth.models import User
from django import forms







class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control','style': 'width:300px;margin-top:5px'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    #Thay đổi label của mật khẩu cách dưới hoặc dưới nữa , 2 cách
    # password1 = forms.CharField(label="Mật khẩu",
    #                             strip=False,
    #                             widget=forms.PasswordInput,
    #                             help_text=password_validation.password_validators_help_text_html(),)

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')
        # widgets ={
        #     'username': forms.TextInput(attrs={'class': 'form-control'}),
        #     'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        # }
    def __init__(self,*args,**kwargs):
        super(SignUpForm, self).__init__(*args,**kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        #Thay đổi label của password
        self.fields['password1'].label = 'Mật khẩu'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].label = 'Nhập lại mật khẩu'




class EditProfileForm(UserChangeForm):
    username=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control','disabled':'true'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_joined = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control','disabled':'true'}))

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','date_joined']





