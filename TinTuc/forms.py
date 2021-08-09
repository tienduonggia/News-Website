from django import forms
from .models import Post
from django.forms import ModelForm
from .models import Contact

class PostForm_Add(forms.ModelForm):
    class Meta:
        model = Post
        # fields= '__all__'
        fields= ['title','category','header_image','author','body']
        widgets ={
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            # 'author': forms.Select(attrs={'class': 'form-control'}),
            #đây mình sẽ ẩn vlue id người dùng này, id elder này mình sẽ chuyển sang bên front end biết là id của inputtext này tên là elder , và bên kia sẽ chuyền gtri vào
            'author': forms.TextInput(attrs={'class': 'form-control','value': '','id': 'elder' , 'type':'hidden'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),

        }

class PostForm_Update(forms.ModelForm):
    class Meta:
        model = Post
        fields= ['title','header_image','category','body']

        widgets ={
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }




class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'