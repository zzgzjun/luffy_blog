from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib import auth
import random
from . import forms, models
from django.contrib.auth.hashers import make_password


# Create your views here.


def index(request):
    return render(request, "page/index.html")


def myforms(request):
    return render(request, "page/myforms.html")


def login(request):
    if request.method == "POST":
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        valid_code = request.POST.get("valid_code")

        resp = {"user": None, "msg": None}

        valid_code_str = request.session.get("valid_code_str")
        if valid_code.upper() == valid_code_str.upper():
            user = auth.authenticate(username=user, password=pwd)
            if user:
                auth.login(request, user)
                resp["user"] = user.username
            else:
                resp["msg"] = "用户名或密码错误！"
        else:
            resp["msg"] = "验证码错误!"
        return JsonResponse(resp)
    return render(request, "login.html")


def register(request):
    resp = {"user": None, "msg": None}
    if request.is_ajax():
        form = forms.UserForm(request.POST)
        if form.is_valid():
            resp["user"] = form.cleaned_data.get("user")
            user = form.cleaned_data.get("user")
            pwd = form.cleaned_data.get("pwd")
            email = form.cleaned_data.get("email")
            avatar_obj = request.FILES.get("avatar")
            # if avatar_obj:
            #     models.UserInfo.objects.create(username=user,password=make_password(pwd),email=email,avatar=avatar_obj)
            # else:
            #     models.UserInfo.objects.create(username=user, password=pwd, email=email)
            extra = {}
            if avatar_obj:
                extra["avatar"] = avatar_obj
                models.UserInfo.objects.create(username=user, password=make_password(pwd), email=email, **extra)
        else:
            resp["msg"] = form.errors
        return JsonResponse(resp)
    form = forms.UserForm()
    return render(request, "register.html", {"form": form})

from blog.utils.validCode import get_valid_code_img
def get_valid_code(request):
    data=get_valid_code_img(request)
    return HttpResponse(data)
