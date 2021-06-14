import datetime, pytz
from django.contrib.auth.forms import AuthenticationForm
from django.http.response import HttpResponseRedirect
from app.forms import LoginForm, PostForm, ProfileForm, RegisterForm
from app.models import Author, Post
from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
# Create your views here.

def logout_views(req):
    auth_logout(req)
    return redirect('/login/')

    
class RegisterView(View):
    # pass
    models = Author
    form = RegisterForm
    initial = {'key': 'value'}
    template_name = 'app/register.html'

    def render(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def get(self, request, *args, **kwargs):
       
        self.form = self.form(initial=self.initial)
        print(self.form)
        self.context = {'form': self.form}
        return self.render(request)

    def post(self, request, *args, **kwargs):
        self.form = self.form(request.POST, request.FILES,)
        if self.request.user.is_authenticated:
            return redirect('home')

        if self.form.is_valid():
            
            self.form.save()
            self.profile_image = self.form.cleaned_data.get('profile_image')
            self.username = self.form.cleaned_data.get('username')
            messages.success(
                request, f'Your account:{self.username} has been created! Your ar now able to login.')
            return redirect('login')
        else:
            # self.form = self.form(initial=self.initial)
            print(self.form)
        self.context = {'form': self.form}
        return self.render(request)
        
class LoginView(View):
    models = Author
    form = LoginForm
    initial = {'key': 'value'}
    template_name = 'app/login.html'

    def render(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def get(self, request, *args, **kwargs):
       
        self.form = self.form(initial=self.initial)
        self.context = {'form': self.form}
        return self.render(request)

    def post(self, request, *args, **kwargs):
        self.form = self.form(request.POST)
        self.username = request.POST.get('username', '')
        self.password = request.POST.get('password', '')
        self.user = authenticate(username=self.username, password=self.password)
        # if request.method == 'POST':
        if self.request.user.is_authenticated:
            return redirect('member_all')
        if self.user is not None:

            if self.user.is_active:
                auth_login(request, self.user)
                messages.success(request, "You have logged in!")
                return HttpResponseRedirect('/')
    
            else:
                messages.warning(request, "Your account is disabled!")
                return redirect('/login/')
        else:
            messages.warning(
                request, "Warning!The username or password are not valid!")
        self.context ={'form':self.form}
        return self.render(request)

class ProfileView(LoginRequiredMixin,View):
    models = Author
    form = ProfileForm
    template_name = 'app/profile.html'
    success_url ="profile"

    def render(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def get(self, request, *args, **kwargs):
        self.profile = self.models.objects.filter(pk=request.user.pk).first()
        self.post = self.models.objects.all()
        self.context = {'profiles':self.profile}
        return self.render(request)

class EditProfileView(LoginRequiredMixin,View):
    models = Author
    forms = ProfileForm
    template_name = 'app/editprofile.html'
    success_url ="profile"

    def render(self, request,username, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def get(self, request,username, *args, **kwargs):
        self.profile =self.models.objects.get(username=username)
        if self.request.user == self.profile:
            self.form = self.forms(instance=self.profile)
        else:
            messages.info(request, "ของคนอื่นแก้ไม่ได้")
            return redirect('home')
        self.context = {'form':self.form,'profiles':self.profile}
        return self.render(request, username)

    def post(self, request,username, *args, **kwargs):
        self.profile =self.models.objects.get(username=username)
        if self.request.user == self.profile:
            self.form = self.forms( request.POST, request.FILES, instance=self.profile)
            if self.form.is_valid():
                self.form.save()
                messages.success(request, "Your account has been updated!")
                return redirect('/profile/')
            else:
                messages.success(request, "จะไปแก้ของคนอื่นได้ไง")
           
        else:
            self.form = self.forms( instance=self.request.user)
           
        self.context = {'form':self.form}
        return self.render(request,username)


class HomeView(LoginRequiredMixin,View):
    models = Post
    author_models = Author
    form = PostForm
    initial = {'key': 'value'}
    template_name = 'app/index.html'
    success_url ="home"


    def render(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return redirect('login')
        tz = pytz.timezone('Asia/Bangkok')
        self.form = self.form(initial=self.initial)
        self.post = self.models.objects.filter(author=request.user)
        self.author = self.author_models.objects.filter(pk=request.user.pk).first()
        this_month = datetime.datetime.now(tz)
        month_name = 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[this_month.month]
        thai_year = this_month.year + 543
        this_month2 = datetime.datetime.now().month
        self.filterAll = self.models.objects.filter(author=request.user,date_posted__month=this_month2)
        self.filterPossi = self.models.objects.filter(author=request.user,sentiment="positive",date_posted__month=this_month2)
        self.filterNeg = self.models.objects.filter(author=request.user,sentiment="negative",date_posted__month=this_month2)
        self.calPossi = (len(self.filterPossi)*100)/len(self.filterAll)
        self.calNeg = (len(self.filterNeg)*100)/len(self.filterAll)
        roundPossi = round(self.calPossi)
        roundNeg = round(self.calNeg)
    
        
        
        self.context = {'roundPossi':roundPossi,'roundNeg':roundNeg,'month_name':month_name,'filter':self.filterAll,'form': self.form,'post': self.post,'author': self.author}
        
        return self.render(request)
        

class EditView(LoginRequiredMixin,View):
    models = Post
    success_url = "edit"
    forms = PostForm
    template_name ="app/edit.html"

    def render(self, request,pk, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def get(self, request,pk, *args, **kwargs):
        self.post =self.models.objects.get(pk=pk)
        if self.request.user == self.post.author:
            self.form = self.forms(instance=self.post)
        else:
            messages.info(request, "ของคนอื่นแก้ไม่ได้")
            return self.redirect(request,pk)
        self.context = {'form':self.form,'posts':self.post}
        return self.render(request, pk)

    def post(self, request,pk, *args, **kwargs):
        self.post =self.models.objects.get(pk=pk)
        if self.request.user == self.post.author:
            self.form = PostForm( request.POST, request.FILES, instance=self.post)
            sentiment = []
        
            context = {}
            if self.form.is_valid():
                # print (self.form.instance)
                moji_list =[['🙂','😄','😁','😆','😀','😊','😃'],
                ['😢','😥','😰','😓','🙁','😟','😞','😔','😣','😫','😩'],
                ['😡','😠','😤','😖'],
                ['🙄','😒','😑','😕'],
                ['😱'],
                ['😨','😧','😦'],
                ['😮','😲','😯'],
                ['😴','😪'],
                ['😋','😜','😝','😛'],
                ['😍','💕','😘','😚','😙','😗'],
                ['😌'],
                ['😐'],
                ['😷'],
                ['😳'],
                ['😵'],
                ['💔'],
                ['😎','😈'],
                ['🙃','😏','😂','😭'],
                ['😬','😅','😶'],
                ['😉'],
                ['💖','💙','💚','💗','💓','💜','💘','💛'],
                ['😇']]
                url = "https://api.aiforthai.in.th/emoji"
                text = self.form.instance
                params = {'text':text}
            
                headers = {
                    'Apikey': "3gCn6fXC0WwqfKGJbS309aWqnXiyyf1M"
                    }
                response = requests.get(url, params=params, headers=headers,)
        
                keys=response.json().keys()
                self.emoji = [moji_list[int(k)][0] for k in keys]
                emoji =  ""
                for i in self.emoji:
                    emoji += i
            
    
                url = "https://api.aiforthai.in.th/ssense"
                
                text = self.form.instance
                
                
                print(f'___text____{text}___________')
                data = {'text':text}
                
                headers = {
                    'Apikey': "3gCn6fXC0WwqfKGJbS309aWqnXiyyf1M"
                    }
        
                self.response = requests.post(url, data=data, headers=headers)
                self.polarity = (self.response.json()['sentiment']['polarity'])
                self.score = (self.response.json()['sentiment']['score'])
                print(self.polarity,self.score,self.emoji )
                self.form.instance.sentiment =  self.polarity
                self.form.instance.score  =self.score
                self.form.instance.emoji =emoji
                self.form.instance.sentiment =  self.polarity
                self.form.instance.author = self.request.user
                self.form.save()
                # print(self.form)
                messages.success(request, 'เพิ่มสำเร็จ')
                return redirect(f'/detail/{self.post.pk}/')

       
           
            else:
                self.form = self.form(instance=self.request.user)
            self.context = {'form':self.form}
            return self.render(request,pk)
        return self.render(request.pk)
           
              

class DeleteView(LoginRequiredMixin,View):
    models = Post
    success_url = "total"
    

    def redirect(self,request,pk, *args, **kwargs):
        return redirect(self.success_url)

    def get(self, request, pk,*args, **kwargs):
        
        self.post = self.models.objects.get(pk=pk)
        print(self.post)
        if self.request.user == self.post.author:
            self.models.objects.filter(pk=pk).delete()
            messages.success(request, 'delete success!')
            return self.redirect(request,pk)
        messages.warning(request, 'คุณเป็นใครจะมาลบของฉัน')
        return self.redirect(request,pk)

class DetailView(LoginRequiredMixin,View):
    models = Post
    template_name = 'app/detail.html'

    def render(self, request,pk, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def get(self, request, pk,*args, **kwargs):
        self.post = self.models.objects.filter(author=request.user,pk=pk).first()
        print(self.post)
        self.context = {'post':self.post}
        return self.render(request,pk)

class CreateView(LoginRequiredMixin,View):
    models = Post
    form = PostForm
    author_models = Author
    initial = {'key': 'value'}
    template_name = 'app/create.html'
    success_url ="total"


    def render(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def get(self, request, *args, **kwargs):
      
        self.form = self.form(initial=self.initial)
        self.post = self.models.objects.filter(author=request.user)
        self.author = self.author_models.objects.filter(pk=request.user.pk).first()
        self.context = {'form': self.form,'post': self.post,'author': self.author}
        
        return self.render(request)

    def post(self, request, *args, **kwargs):
        self.form = self.form(request.POST, request.FILES)
        sentiment = []
        
        context = {}
        if self.form.is_valid():
            # print (self.form.instance)
            moji_list =[['🙂','😄','😁','😆','😀','😊','😃'],
            ['😢','😥','😰','😓','🙁','😟','😞','😔','😣','😫','😩'],
            ['😡','😠','😤','😖'],
            ['🙄','😒','😑','😕'],
            ['😱'],
            ['😨','😧','😦'],
            ['😮','😲','😯'],
            ['😴','😪'],
            ['😋','😜','😝','😛'],
            ['😍','💕','😘','😚','😙','😗'],
            ['😌'],
            ['😐'],
            ['😷'],
            ['😳'],
            ['😵'],
            ['💔'],
            ['😎','😈'],
            ['🙃','😏','😂','😭'],
            ['😬','😅','😶'],
            ['😉'],
            ['💖','💙','💚','💗','💓','💜','💘','💛'],
            ['😇']]
            url = "https://api.aiforthai.in.th/emoji"
            text = self.form.instance
            params = {'text':text}
        
            headers = {
                'Apikey': "3gCn6fXC0WwqfKGJbS309aWqnXiyyf1M"
                }
            response = requests.get(url, params=params, headers=headers,)
    
            keys=response.json().keys()
            self.emoji = [moji_list[int(k)][0] for k in keys]
            emoji =  ""
            for i in self.emoji:
                emoji += i
        
 
            url = "https://api.aiforthai.in.th/ssense"
            
            text = self.form.instance
             
            
            print(f'___text____{text}___________')
            data = {'text':text}
            
            headers = {
                'Apikey': "3gCn6fXC0WwqfKGJbS309aWqnXiyyf1M"
                }
    
            self.response = requests.post(url, data=data, headers=headers)
            self.polarity = (self.response.json()['sentiment']['polarity'])
            self.score = (self.response.json()['sentiment']['score'])
            print(self.polarity,self.score,self.emoji )
            self.form.instance.sentiment =  self.polarity
            self.form.instance.score  =self.score
            self.form.instance.emoji =emoji
            self.form.instance.sentiment =  self.polarity
            self.form.instance.author = self.request.user
            self.form.save()
            # print(self.form)
            messages.success(request, 'เพิ่มสำเร็จ')
            return redirect(self.success_url)

       
           
        else:
            self.form = self.form(instance=self.request.user)
        self.context = {'form':self.form}
        return self.render(request)
    
class TotalView(LoginRequiredMixin,View):
    models = Post
    author_models = Author
    template_name = 'app/total.html'
    success_url ="total"


    def render(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)


    def get(self, request, *args, **kwargs):
        import random
        from django.core.cache import cache
        import datetime
  
        self.post = self.models.objects.filter(author=request.user)
        self.author = self.author_models.objects.filter(pk=request.user.pk).first()

        list1=[]
        for i in self.post:
            
            list1[:0]=i.emoji
            # list1[:]=i.emoji
            # print(i.id,i.emoji,len(list1[:0]))
        # print(list1)
        r=random.choice(list1)
        if request.GET.get('month'):
            p=self.models.objects.filter(author=request.user)    
            getmonth = request.GET.get('month')
            print(getmonth)
            filterM = self.models.objects.filter(author=request.user,date_posted__month=getmonth)
            print(filterM)
            self.context = {'filter': filterM}
            return self.render(request) 
        else:
            self.context = {'emo': r,'post': self.post,'author': self.author}
            return self.render(request)
       
        
        # self.context = {'emo': r,'post': self.post,'author': self.author}
        
        # return self.render(request)