from django.db import models
from django.contrib.auth.models import User,AbstractUser

# Create your models here.


class UserInfo(AbstractUser):
    """用户信息"""
    nid=models.AutoField(primary_key=True)
    telephone=models.CharField(max_length=11,null=True,unique=True)
    avatar=models.FileField(upload_to='avatars/',default="/avatars/default.png")
    create_time=models.DateTimeField(verbose_name='创建时间',auto_now_add=True)

    def __str__(self):
        return self.username


class Blog(models.Model):
    """博客信息表（个人站点表）"""
    nid = models.AutoField(primary_key=True)
    title=models.CharField(max_length=64,verbose_name='个人博客标题')
    site_name=models.CharField(max_length=64,verbose_name='站点名称')
    theme=models.CharField(max_length=32,verbose_name='博客主题')

    def __str__(self):
        return self.title


class Category(models.Model):
    nid=models.AutoField(primary_key=True)
    title=models.CharField(verbose_name="分类标题",max_length=32)
    blog=models.ForeignKey(verbose_name="所属博客",to="Blog",to_field='nid')

    def __str__(self):
        return self.title


class Tag(models.Model):
    nid=models.AutoField(primary_key=True)
    title=models.CharField(verbose_name="标签名称",max_length=32)
    blog=models.ForeignKey(verbose_name="所属博客",to="Blog",to_field='nid')

    def __str__(self):
        return self.title


class Article(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="文章标题", max_length=50)
    desc = models.CharField(verbose_name="文章描述", max_length=255)
    content = models.TextField()

    comment_count=models.IntegerField(default=0)
    up_count=models.IntegerField(default=0)
    down_count=models.IntegerField(default=0)

    user=models.ForeignKey(verbose_name="作者",to="UserInfo",to_field="nid")
    category=models.ForeignKey(to="Category",to_field="nid",blank=True)
    tags=models.ManyToManyField(
        to="Tag",
        through="Article2Tag",
        through_fields=("article","tag")
    )


    def __str__(self):
        return self.title


class Article2Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    article=models.ForeignKey(verbose_name="文章",to="Article",to_field="nid")
    tag=models.ForeignKey(verbose_name="标签",to="Tag",to_field="nid")

    class Meta:
        unique_together=[('article','tag')]

    def __str__(self):
        v=self.article.title+"---"+self.tag.title
        return v


class ArticleUpDown(models.Model):
    """文章点赞表"""
    nid = models.AutoField(primary_key=True)
    user=models.ForeignKey("UserInfo",null=True)
    article=models.ForeignKey("Article",null=True)
    is_up=models.BooleanField(default=True)

    class Meta:
        unique_together = [('article', 'user')]


class Comment(models.Model):
    """评论表"""
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name="评论文章", to="Article", to_field="nid")
    user = models.ForeignKey(verbose_name="评论者", to="UserInfo", to_field="nid")
    content=models.CharField(verbose_name="评论内容",max_length=255)
    create_time=models.DateTimeField("创建市级",auto_now_add=True)
    parent_comment=models.ForeignKey('self',null=True)

    def __str__(self):
        return self.content
