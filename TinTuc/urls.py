from django.contrib import admin
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('detail/<int:pk>',NewsDetailView.as_view(),name="news_detail"),
    path('addnews/',AddNewsView.as_view(),name="add_news"),
    path('detail/edit/<int:pk>',UpdateNewsView.as_view(),name="update_news"),
    path('detail/<int:pk>/delete',DeleteNewsView.as_view(),name="delete_news"),
    #Nếu ta dùng view tự tạo thì sẽ k có as_view
    path('category/<str:cats>',CategoryView,name="category"),
    path('like/<int:pk>', LikeView, name='like_news'),
    path('search/',SearchView,name="search_news"),
    path('contact/',ContactView,name="contact_news"),

]
