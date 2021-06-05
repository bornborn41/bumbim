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
        if self.request.user.is_authenticated:
            return redirect('home')
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
            self.form = self.form(initial=self.initial)
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
        if self.request.user.is_authenticated:
            return redirect('home')
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
    form = PostForm
    initial = {'key': 'value'}
    template_name = 'app/index.html'
    success_url ="home"


    def render(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return redirect('login')
        self.form = self.form(initial=self.initial)
        self.post = self.models.objects.filter(author=request.user)
        self.context = {'form': self.form,'post': self.post}
        
        return self.render(request)

    def post(self, request, *args, **kwargs):
        self.form = self.form(request.POST, request.FILES)
        if self.form.is_valid():
            
            self.form.instance.author = self.request.user
            self.form.save()
            messages.success(
                request, ' created success!')
            return redirect(self.success_url)
           
        else:
            self.form = self.form(instance=self.request.user)
        self.context = {'form':self.form}
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
            if self.form.is_valid():
                self.form.instance.author = self.request.user
                self.form.save()
                messages.success(request, "Your account has been updated!")
                return redirect(f'/detail/{pk}/')
            else:
                messages.success(request, "จะไปแก้ของคนอื่นได้ไง")
           
        else:
            self.form = PostForm( instance=self.post)
           
        self.context = {'form':self.form}
        return self.render(request,pk)

class DeleteView(LoginRequiredMixin,View):
    models = Post
    success_url = "home"
    

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

    
        