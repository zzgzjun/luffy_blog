import random


def get_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def get_valid_code_img(request):
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
    from PIL import Image, ImageDraw, ImageFont
    from io import BytesIO
    img = Image.new("RGB", (270, 40), color=get_random_color())

    draw = ImageDraw.Draw(img)
    fzht_font = ImageFont.truetype("static/font/fzht.ttf", size=32)

    # 生成5个随机字符
    valid_code_str = ""
    for i in range(5):
        random_num = str(random.randint(0, 9))
        random_low_alpha = chr(random.randint(95, 122))
        random_upper_alpha = chr(random.randint(65, 90))
        random_char = random.choice([random_num, random_low_alpha, random_upper_alpha])
        draw.text((i * 50 + 20, 5), random_char, get_random_color(), font=fzht_font)
        # 保存随机字符串
        valid_code_str += random_char
    # 生成噪点噪线
    width = 270
    height = 40
    # for i in range(12):
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=get_random_color())

    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())
    # 随机字符串存入session中
    request.session['valid_code_str'] = valid_code_str
    # 内存处理
    f = BytesIO()
    img.save(f, "png")
    data = f.getvalue()
    return data
