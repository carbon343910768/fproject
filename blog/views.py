from django.shortcuts import render, redirect, HttpResponse
from django.core.exceptions import ValidationError
from django.contrib import auth
from .models import MyUser  # 导入django自带的user表
from . import models
from django import forms  # 导入表单
import datetime, re


def email_unique(value):
    mobile_re = re.compile(r'\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}')
    if not mobile_re.match(value):
        raise ValidationError('enter a valid email address.')
    email_model = list(MyUser.objects.all().values_list('email'))
    for i in email_model:
        if value in i:
            raise ValidationError('email already taken.')


def username_unique(value):
    username_model = list(MyUser.objects.all().values_list('username'))
    mobile_re = re.compile(r'^[a-z]+$')
    if not mobile_re.match(value):
        raise ValidationError('username has illegal characters.')
    for i in username_model:
        if value in i:
            raise ValidationError('username already taken.')


def email_not_exist(value):
    exist = False
    email_model = list(MyUser.objects.all().values_list('email'))
    for i in email_model:
        if value in i:
            exist = True
    if not exist:
        raise ValidationError('email not found.')


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "your email", "value": "", "required": "required", }),
        validators=[email_not_exist],
        max_length=100,
        error_messages={'required': u'email is empty', 'invalid': u'Invalid email!'})
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "your password", "value": "", "required": "required", }),
        label='password',
        min_length=6, error_messages={'min_length': u'password is invalid.',
                                      'required': u'pwd is empty'})


class UserForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "your email", "value": "", "required": "required"}),
        validators=[email_unique],
        label='email',
        max_length=100,
        error_messages={'required': u'email is empty'})
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "your username", "value": "", "required": "empty", }),
        validators=[username_unique],
        label='username',
        max_length=100)
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "your password", "value": "", "required": "pwd is empty", }),
        label='password',
        error_messages={'min_length': u'password too short.',
                        'required': u'pwd is empty'})
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "your password again", "value": "",
                                          "required": "required", }),
        label='cpassword',
        error_messages={'required': u'pwd is empty'})

    def clean(self):
        pwd = self.cleaned_data['password']
        pwdc = self.cleaned_data['password_confirmation']
        if len(pwd) <6:
            self.add_error('password', 'password too short.')
        if pwd != pwdc:
            self.add_error('password_confirmation', 'password mismatch.')
        return self.cleaned_data


class UpdateForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "your email", "value": "", "required": "required"}),
        validators=[email_unique],
        label='email',
        max_length=100,
        error_messages={'required': u'email is empty'})


class UpdatePwdForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "your old password", "value": "", "required": "pwd is empty", }),
        label='opassword',
        error_messages={'min_length': u'password too short.',
                        'required': u'pwd is empty'})
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "your password", "value": "", "required": "pwd is empty", }),
        label='password',
        error_messages={'min_length': u'password too short.',
                        'required': u'pwd is empty'})
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "your password again", "value": "",
                                          "required": "required", }),
        label='cpassword',
        error_messages={'required': u'pwd is empty'})

    def clean(self):
        pwd = self.cleaned_data['password']
        pwdc = self.cleaned_data['password_confirmation']
        if len(pwd) <6:
            self.add_error('password', 'password too short.')
        if pwd != pwdc:
            self.add_error('password_confirmation', 'password mismatch.')
        return self.cleaned_data

class postBlogForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "post_content", "placeholder": "your idea", "value": "", "required": "required"}),
        label='blog_content',
        max_length=300,
        error_messages={'required': u'content is empty'}
    )

def login(request):
    uf = LoginForm()
    if request.method == 'POST':
        uf = LoginForm(request.POST)
        if uf.is_valid():
            # 获取表单数据
            email = uf.cleaned_data['email']  # cleaned_data类型是字典，里面是提交成功后的信息
            password = uf.cleaned_data['password']
            re = auth.authenticate(email=email, password=password)  # 用户认证
            if re is not None:  # 如果数据库里有记录（即与数据库里的数据相匹配或者对应或者符合）
                auth.login(request, re)  # 登陆成功
                return redirect('/me', {'user': re})
            else:
                return render(request, 'login.html', {'uf': uf, 'error_msg': 'password is invalid.'})
    return render(request, 'login.html', {'uf': uf})


def register(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)  # 包含用户名和密码
        if uf.is_valid():
            # 获取表单数据
            email = uf.cleaned_data['email']  # cleaned_data类型是字典，里面是提交成功后的信息
            password = uf.cleaned_data['password']
            cpassword = uf.cleaned_data['password_confirmation']
            username = uf.cleaned_data['username']
            # 添加到数据库
            if cpassword == password:
                MyUser.objects.create_user(email=email, username=username, password=password,
                                           created_at=datetime.datetime.now().strftime('%Y-%m-%d'))
                return redirect('/login')
            else:
                return render(request, 'register.html', {'uf': uf, })
        else:
            return render(request, 'register.html', {'uf': uf, })
    else:
        # 如果不是post提交数据，就不传参数创建对象，并将对象返回给前台，直接生成input标签，内容为空
        uf = UserForm()
        return render(request, 'register.html', {'uf': uf})


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return render(request, 'logout.html')
    else:
        return redirect('/login')


def me(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html')
    else:
        return redirect('/login')


def home(request):
    if request.user.is_authenticated:
        return redirect('/me')
    else:
        return render(request, 'home.html')


def emailupdate(request):
    if request.user.is_authenticated:
        uf = UpdateForm()
        if request.method == 'POST':
            uf = UpdateForm(request.POST)
            if uf.is_valid():
                # 获取表单数据
                oldemail = request.user
                email = uf.cleaned_data['email']  # cleaned_data类型是字典，里面是提交成功后的信息
                username = MyUser.objects.get(email=oldemail).username
                MyUser.objects.filter(username=username).update(email=email)
                return redirect('/me')
            else:
                return render(request, 'email_update.html', {'uf': uf})
        return render(request, 'email_update.html', {'uf': uf})
    else:
        return render(request, 'home.html')


def passwordupdate(request):
    if request.user.is_authenticated:
        uf = UpdatePwdForm()
        if request.method == 'POST':
            uf = UpdatePwdForm(request.POST)
            if uf.is_valid():
                # 获取表单数据
                oldpwd = uf.cleaned_data['old_password']
                pwd = uf.cleaned_data['password']
                email = request.user
                re = auth.authenticate(email=email, password=oldpwd)  # 用户认证
                if re is not None:
                    auth.logout(request)
                    user=MyUser.objects.get(email=email)
                    user.set_password(pwd)
                    user.save()
                    return redirect('/login')
                else:
                    return render(request, 'password_update.html', {'uf': uf, 'error_msg':'invalid password.'})
            else:
                return render(request, 'password_update.html', {'uf': uf})
        return render(request, 'password_update.html', {'uf': uf})
    else:
        return render(request, 'home.html')

def post_blog(request):
    if request.user.is_authenticated:
        uf = postBlogForm()
        blog = models.blog.objects.all().order_by('-id')
        if request.method == 'POST':
            uf = postBlogForm(request.POST)
            if uf.is_valid():
                # 获取表单数据
                content = uf.cleaned_data['content']
                username = request.user.username
                post_time = datetime.datetime.now()
                models.blog.objects.create(username=username,content=content,pub_date=post_time)
                return redirect('../post_blog')
            else:
                return render(request, 'postblog1.html', {'uf': uf, 'post':blog,'username':request.user.username})
        return render(request, 'postblog1.html', {'uf': uf, 'post':blog,'username':request.user.username})
    else:
        return redirect('/login')

def digg(request):
    if request.user.is_authenticated:
        print(request.GET.__getitem__('is_like'))
        if request.GET.__getitem__('is_like') == 'true':
            if not models.like.objects.filter(username=request.user.username, likeblog=request.GET.__getitem__('article_id')):
                models.like.objects.create(username=request.user.username, likeblog=request.GET.__getitem__('article_id'))
                like = models.like.objects.filter(likeblog=request.GET.__getitem__('article_id')).count()
                models.blog.objects.filter(id=request.GET.__getitem__('article_id')).update(like=like)
                return HttpResponse("1")
            else:
                return HttpResponse("2")
        else:
            models.like.objects.filter(username=request.user.username, likeblog=request.GET.__getitem__('article_id')).delete()
            return HttpResponse("3")

def delete(request):
    if request.user.is_authenticated:
        print(request.GET.__getitem__('is_delete'))
        if request.GET.__getitem__('is_delete') == 'true':
            models.blog.objects.filter(username=request.user.username, id=request.GET.__getitem__('article_id')).delete()
            return HttpResponse("1")
        else:
            return HttpResponse("3")

