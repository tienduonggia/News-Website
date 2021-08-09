from django.contrib.auth import authenticate
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView,LoginView
from django.urls import reverse_lazy

from TinTuc.models import Category
from TinTuc.views import AddNewsView
from .forms import SignUpForm, EditProfileForm
from django.contrib.messages.views import SuccessMessageMixin





class PasswordsChange(SuccessMessageMixin,PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('edit_profile')
    template_name = 'registration/change-password.html'
    success_message = "Đã thay đổi thành công!!!"
    def get_context_data(self, *args ,**kwargs):
        context = super(PasswordsChange,self).get_context_data(*args ,**kwargs)
        cat_menu = Category.objects.all()
        context['cat_menu'] = cat_menu
        return context



# class Login(LoginView):
#     form_class = LoginForm



class UserRegisterView(generic.CreateView):
    # form class dưới là form mặc định tự tạo của django(chỉ có user name password vaf confpass), ta sẽ dùng cái mình tự tạo sẽ đầy đủ hơn
    # form_class = UserCreationForm
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    def get_context_data(self, *args ,**kwargs):
        context = super(UserRegisterView,self).get_context_data(*args ,**kwargs)
        cat_menu = Category.objects.all()
        context['cat_menu'] = cat_menu
        return context

class UserEditView(generic.UpdateView):
    # form class dưới là form mặc định tự tạo của django(chỉ có user name password vaf confpass), ta sẽ dùng cái mình tự tạo sẽ đầy đủ hơn
    # form_class = UserChangeForm
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('home')
    def get_context_data(self, *args ,**kwargs):
        context = super(UserEditView,self).get_context_data(*args ,**kwargs)
        cat_menu = Category.objects.all()
        context['cat_menu'] = cat_menu
        return context

    #trả về kq cho bik ng dùng đang là ai
    def get_object(self):
        return self.request.user







