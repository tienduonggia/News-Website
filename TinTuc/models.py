from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.urls import reverse
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        #Khi viết bài xong nhấn button gửi sẽ chuyển sang trang chi tiết với pk vừa tạo hoặc 1 url nào đó , KH ÁP DỤNG VỚI DELETE
        # return reverse('news_detail',args=(str(self.id))) , chuyển về trang detail chính nó
        return reverse('home')


class Post(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    header_image = models.ImageField(null=True, blank=True, upload_to='images/')
    # body = models.TextField()
    body = RichTextField(blank=True,null = True)
    news_date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,related_name='new_posts',null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    blog_view = models.IntegerField(default=0)

    #hàm này chỉ để return tổng số like của bài đó
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title + ' | ' + str(self.author)

    def get_absolute_url(self):
        #Khi viết bài xong nhấn button gửi sẽ chuyển sang trang chi tiết với pk vừa tạo hoặc 1 url nào đó , KH ÁP DỤNG VỚI DELETE
        # return reverse('news_detail',args=(str(self.id))) , chuyển về trang detail chính nó
        return reverse('home')


class Comment(models.Model):
    post = models.ForeignKey(Post,related_name="comments",on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)


class Contact(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.email

