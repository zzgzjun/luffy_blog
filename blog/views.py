from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.contrib import auth
import random
from . import forms
# Create your views here.


def index(request):
    return render(request,"index.html")


def login(request):
    if request.method=="POST":
        user=request.POST.get("user")
        pwd=request.POST.get("pwd")
        valid_code=request.POST.get("valid_code")

        resp={"user":None,"msg":None}

        valid_code_str=request.session.get("valid_code_str")
        if valid_code.upper()==valid_code_str.upper():
            user=auth.authenticate(username=user,password=pwd)
            if user:
                auth.login(request,user)
                resp["user"]=user.username
            else:
                resp["msg"]="用户名或密码错误！"
        else:
            resp["msg"]="验证码错误!"
        return JsonResponse(resp)
    return render(request,"login.html")


def register(request):
    if request.is_ajax():
        resp={"user":None,"msg":None}
        form = forms.UserForm(request.POST)
        if form.is_valid():
            resp["user"]=form.cleaned_data.get("user")
        else:
            resp["msg"]=form.errors
        return JsonResponse(resp)
    form=forms.UserForm()
    return render(request,"register.html",{"form":form})


def get_validCode_img(request):
    def get_random_color():
        return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    # 方式1
    # with open("luffy.jpg","rb") as f:
    #     data=f.read()
    # 方式2 # pip install pillow
    # 磁盘文件管理
    # from PIL import Image
    # img=Image.new("RGB",(270,40),color=get_random_color())
    # with open("validCode.png","wb") as f:
    #     img.save(f,"png")
    # with open("validCode.png","rb") as f:
    #     data=f.read()

    # 方式3
    # from PIL import Image
    # from io import BytesIO
    # img = Image.new("RGB", (270, 40), color=get_random_color())
    # # 内存处理
    # f= BytesIO()
    # img.save(f,"png")
    # data=f.getvalue()

    # 方式4
    from PIL import Image,ImageDraw,ImageFont
    from io import BytesIO
    img = Image.new("RGB", (270, 40), color=get_random_color())

    draw=ImageDraw.Draw(img)
    fzht_font=ImageFont.truetype("static/font/fzht.ttf",size=32)

    # 生成5个随机字符
    valid_code_str=""
    for i in range(5):
        random_num = str(random.randint(0, 9))
        random_low_alpha = chr(random.randint(95, 122))
        random_upper_alpha = chr(random.randint(65, 90))
        random_char=random.choice([random_num,random_low_alpha,random_upper_alpha])
        draw.text((i*50+20,5),random_char,get_random_color(),font=fzht_font)
        #保存随机字符串
        valid_code_str+=random_char
    # 生成噪点噪线
    width=270
    height=40
    # for i in range(12):
    for i in range(5):
        x1=random.randint(0,width)
        y1 = random.randint(0, height)
        x2=random.randint(0,width)
        y2=random.randint(0,height)
        draw.line((x1,y1,x2,y2),fill=get_random_color())

    for i in range(40):
        draw.point([random.randint(0,width),random.randint(0,height)],fill=get_random_color())
        x=random.randint(0,width)
        y=random.randint(0,height)
        draw.arc((x,y,x+4,y+4),0,90,fill=get_random_color())
    # 随机字符串存入session中
    request.session['valid_code_str']=valid_code_str
    # 内存处理
    f= BytesIO()
    img.save(f,"png")
    data=f.getvalue()

    return HttpResponse(data)
