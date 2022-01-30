from django.db import models
from django.contrib.auth.models import AbstractUser
from bilibili_project.settings import MEDIA_ROOT


# Create your models here.

def upload_to(instance, nickname):
    return '/User_'.join([instance.nickname, nickname])


class User(models.Model):
    # 用户名/密码/邮箱 为默认
    nickname = models.CharField(max_length=30, verbose_name='用户昵称')
    image = models.ImageField(upload_to=upload_to, verbose_name='用户头像', default="Image/default.png")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    condition = models.CharField(max_length=2, verbose_name='用户状态', default='00')
    password = models.CharField(max_length=30, verbose_name='用户密码')
    """
    {
        '-1': '冻结状态',
        '00': '正常注册',
        '01': '正式用户'
    }
    """

    def __str__(self):
        return str(self.nickname)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


class Up(models.Model):  # 头像存的是路径
    fans = models.CharField(max_length=16, verbose_name='粉丝数')
    up_name = models.CharField(max_length=20, verbose_name='up主名称')
    mid = models.CharField(max_length=16, verbose_name='mid')
    sign = models.TextField(verbose_name='个性签名')
    image = models.TextField(verbose_name='up头像', default="Image/default.png")
    update_time = models.DateTimeField(auto_now_add=True, verbose_name='数据更新时间')

    def __str__(self):
        return str(self.up_name)

    class Meta:
        verbose_name = 'up信息'
        verbose_name_plural = verbose_name


class Video(models.Model):
    # 封面存为URL
    type_id = models.CharField(max_length=2, verbose_name='所属分区')
    comment_num = models.CharField(max_length=16, verbose_name='评论数目')
    play = models.CharField(max_length=16, verbose_name='播放量')
    pic = models.TextField(verbose_name='封面', default="Image/default.png")
    description = models.TextField(verbose_name='描述')
    title = models.TextField(verbose_name='标题')
    length = models.TextField(verbose_name='时长')
    bv = models.CharField(max_length=20, verbose_name='bv号')
    update_time = models.DateTimeField(auto_now_add=True, verbose_name='数据更新时间')

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = '视频详情'
        verbose_name_plural = verbose_name


class Up_Video(models.Model):  # up与视频对应表
    up_id = models.ForeignKey(to='Up', to_field='id', on_delete=models.CASCADE)
    video_id = models.ForeignKey(to='Video', to_field='id', on_delete=models.CASCADE)


class User_Up(models.Model):  # 用户与up对应表
    user_id = models.ForeignKey(to='user', to_field='id', on_delete=models.CASCADE)
    up_id = models.ForeignKey(to='Up', to_field='id', on_delete=models.CASCADE)

