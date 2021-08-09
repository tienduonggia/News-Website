from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pip._vendor import requests

from HiuNews import settings
from TinTuc.models import Category, Comment
from .forms import *


def ContactView(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'contact.html')
    form = ContactForm()
    context = {'form': form}
    return render(request, 'contact.html', context)



def LikeView(request,pk):
    post = get_object_or_404(Post,id=request.POST.get('post_id'))
    #Ý tưởng unlike là ta sẽ set like là false khi ng dùng nhấn like sẽ set true ngc lại
    liked = False
    #Nó sẽ filter lại xem trong bài post_like đó có id dùng đó chưa(đã like hay chưa)
    if post.likes.filter(id=request.user.id).exists():
        #nếu mà đã like rồi mà còn nhấn nữa nghĩ là unlike và ta sẽ remove id đó ra khỏi post_like
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('news_detail',args=[str(pk)]))


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    #có dấu trừ thì sắp xếp ngc lại id cuối cùng đưa lên trc , id đầu sẽ đẩy về sau cùng , id là trường của models Post, có thể sắp xếp theo trường date,..
    #ordering = ['-id']
    ordering = ['-news_date']
    def get_context_data(self, *args ,**kwargs):
        global temperature
        context = super(HomeView, self).get_context_data(*args ,**kwargs)
        # Data về thời tiết API
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=209b95762ff977f11831d359b3bf7d80'
        city = 'SaiGon'
        city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types
        temperature = city_weather['main']['temp']
        tempC = int((temperature - 32)/1.8)
        weather = {
            'city' : city,
            'temperature' : tempC,
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }
        # Data về chuyển đổi tiền tệ API
        url_exchange = 'https://v6.exchangerate-api.com/v6/178ceddc14b68ae3205c17aa/latest/USD'
        unit = 'USD'
        current_exchange = requests.get(url_exchange).json()
        money = {
            'unit' : unit,
            'conversion_rates' : current_exchange['conversion_rates']['VND']
        }


        # API về tỷ giá dùng XML của vietcombank
        url_tygia = 'https://tygia.com/json.php?ran=0&gold=0&bank=VIETCOM&date=now'
        tygia_hientai = requests.get(url_tygia)
        tygia_hientai.encoding = 'utf-8-sig'
        decoded_data=tygia_hientai.json()

        a = decoded_data['rates'][0]['value']

        name= []
        buy = []
        transfer = []
        sell = []
        for i in range(len(a)):
            tygiacuatoi = a[i]
            name.append(tygiacuatoi['name'])
            buy.append(tygiacuatoi['buy'])
            transfer.append(tygiacuatoi['transfer'])
            sell.append(tygiacuatoi['sell'])
        api_tygia = zip(name, buy, transfer, sell)


        #API về tin tức mọi nơi
        url_news = 'https://gnewsapi.net/api/search?q=covid-19&language=vi&country=vn&api_token=C9gBxslQ4hLV47SiKAou3Wjslsv1z4qgo9PEulXvzdcoj6SRCvoGm7Mgr4ci'

        unit = 'COVID-19'
        newsapi = requests.get(url_news).json()
        a= newsapi['articles']
        articlesurl = []
        title =[]
        published_datetime=[]
        image_url =[]
        #Muốn lấy hết gai trị torn api thì : len(a), ở đây muốn lấy 10 cái thôi
        for i in range(15):
            myarticles = a[i]
            articlesurl.append(myarticles['article_url'])
            title.append(myarticles['title'])
            published_datetime.append(myarticles['published_datetime'])
            image_url.append(myarticles['image_url'])
        # covid_news = [{
        #     'unit' : unit,
        #     'articlesurl' : newsapi['articles']['article_url'],
        #     'title' : newsapi['articles']['title'],
        #     'published_datetime' : newsapi['articles']['published_datetime'],
        #     'image_url' : newsapi['articles']['image_url'],
        # }]
        myapi = zip(articlesurl,title,published_datetime,image_url)


       #Data về thể loại
        cat_menu = Category.objects.all()

        post_approval = Post.objects.filter(is_approved=True).order_by('-news_date')
        
        #bài thoe thể loại :
        news_giaoduc = Post.objects.filter(category = 1,is_approved=True).order_by('-news_date')
        news_thethao = Post.objects.filter(category = 2,is_approved=True).order_by('-news_date')
        news_congnghe = Post.objects.filter(category = 4,is_approved=True).order_by('-news_date')
        news_thoisu = Post.objects.filter(category = 5,is_approved=True).order_by('-news_date')
        news_gioitre = Post.objects.filter(category = 6,is_approved=True).order_by('-news_date')
        news_game = Post.objects.filter(category = 7,is_approved=True).order_by('-news_date')
        news_amnhac = Post.objects.filter(category = 8,is_approved=True).order_by('-news_date')
        news_kinhte = Post.objects.filter(category = 9,is_approved=True).order_by('-news_date')

        most_view = Post.objects.all().order_by('-blog_view')




        context['most_view'] = most_view
        context['news_giaoduc'] = news_giaoduc
        context['news_thethao'] = news_thethao
        context['news_congnghe'] = news_congnghe
        context['news_thoisu'] = news_thoisu
        context['news_gioitre'] = news_gioitre
        context['news_game'] = news_game
        context['news_amnhac'] = news_amnhac
        context['news_kinhte'] = news_kinhte


        context['tygia'] = api_tygia
        context['covid19api'] = myapi
        context['post_approval'] = post_approval
        context['thoitiet'] =  weather
        context['tiente'] = money
        context['cat_menu'] = cat_menu
        return context


    #tự tạo view dùng def với request
def CategoryView(request,cats):
    category_news = Post.objects.filter(category= cats)
    category_name = Category.objects.all().filter(id = cats)

    cat_menu = Category.objects.all()


    return render(request,'categories.html',{'cats':cats,'category_news':category_news,'category_name': category_name,'cat_menu':cat_menu})


def SearchView(request):
    if request.method == 'POST':
        searchpost = request.POST['searchpost']
        news = Post.objects.filter(title__contains=searchpost)
        return render(request,'search_news.html',{'searchpost':searchpost,'news':news})
    else:
        return render(request,'search_news.html',{})


class NewsDetailView(DetailView):
    model = Post
    template_name = 'news_detail.html'

    def get_object(self):
        obj = super().get_object()
        obj.blog_view += 1
        obj.save()
        return obj

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        body = request.POST['body']
        idpost = request.POST['idpost']
        try:
           a=  Comment.objects.create(post_id=idpost,name=username,body=body)
           a.save()
           return HttpResponseRedirect(reverse('news_detail',args=[str(idpost)]))
        except Exception as e:
            raise e

    def get_context_data(self, *args ,**kwargs):
        context = super(NewsDetailView,self).get_context_data(*args ,**kwargs)
        cat_menu = Category.objects.all()
        #để lấy đc total like của bài đó ta cần pk của bài đó bằng cách gét pk dưới 9a6y rồi sau đó gọi lại hàm total đã tạo ở moedl
        stuff = get_object_or_404(Post,id=self.kwargs['pk'])

        #hàm trong model
        total_likes = stuff.total_likes()

        #Trên là dùng backend, đây hiển thị ra frontend
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked=True

        hot_post = Post.objects.all().order_by('-news_date')
        total_cmt = Comment.objects.all().filter(post_id=self.kwargs['pk']).count()


        context['total_cmt'] = total_cmt
        context['hot_post'] = hot_post
        context['liked'] = liked
        context['total_likes']= total_likes
        context['cat_menu'] = cat_menu
        return context

class AddNewsView(CreateView):
    model = Post
    template_name = 'add_news.html'
    #Vì mình đã tạo các trường trong form mục đích làm đẹp hơn, nên ta kh cần khai báo 2 tah82ng dưới
    form_class = PostForm_Add

    #Lấy theo từng trường mình cần
    # fields= ('title','body')

    #Lấy tất cả các trường
    #fields = '__all__'
    def get_context_data(self, *args ,**kwargs):
        context = super(AddNewsView,self).get_context_data(*args ,**kwargs)
        cat_menu = Category.objects.all()
        context['cat_menu'] = cat_menu
        return context

class UpdateNewsView(UpdateView):
    model = Post
    template_name = 'update_news.html'
    form_class = PostForm_Update

    def get_context_data(self, *args ,**kwargs):
        context = super(UpdateView,self).get_context_data(*args ,**kwargs)
        cat_menu = Category.objects.all()
        context['cat_menu'] = cat_menu
        return context

class DeleteNewsView(DeleteView):
    model = Post
    template_name = 'delete_news.html'
    #Vì khi nhấn nút delete xong nó k biết chuyển hướng về trang nào nên cần dòng code này
    success_url = reverse_lazy('home')

    def get_context_data(self, *args ,**kwargs):
        context = super(DeleteView,self).get_context_data(*args ,**kwargs)
        cat_menu = Category.objects.all()
        context['cat_menu'] = cat_menu
        return context