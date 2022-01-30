# Generated by Django 3.2.9 on 2021-12-16 15:01

from django.db import migrations, models
import django.db.models.deletion
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Up',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fans', models.CharField(max_length=16, verbose_name='粉丝数')),
                ('up_name', models.CharField(max_length=20, verbose_name='up主名称')),
                ('mid', models.CharField(max_length=16, verbose_name='mid')),
                ('sign', models.TextField(verbose_name='个性签名')),
                ('image', models.TextField(default='Image/default.png', verbose_name='up头像')),
                ('update_time', models.DateTimeField(auto_now_add=True, verbose_name='数据更新时间')),
            ],
            options={
                'verbose_name': 'up信息',
                'verbose_name_plural': 'up信息',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=30, verbose_name='用户昵称')),
                ('image', models.ImageField(default='Image/default.png', upload_to=user.models.upload_to, verbose_name='用户头像')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('condition', models.CharField(default='00', max_length=2, verbose_name='用户状态')),
                ('password', models.CharField(max_length=30, verbose_name='用户密码')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_id', models.CharField(max_length=2, verbose_name='所属分区')),
                ('comment_num', models.CharField(max_length=16, verbose_name='评论数目')),
                ('play', models.CharField(max_length=16, verbose_name='播放量')),
                ('pic', models.TextField(default='Image/default.png', verbose_name='封面')),
                ('description', models.TextField(verbose_name='描述')),
                ('title', models.TextField(verbose_name='标题')),
                ('length', models.TextField(verbose_name='时长')),
                ('bv', models.CharField(max_length=20, verbose_name='bv号')),
                ('update_time', models.DateTimeField(auto_now_add=True, verbose_name='数据更新时间')),
            ],
            options={
                'verbose_name': '视频详情',
                'verbose_name_plural': '视频详情',
            },
        ),
        migrations.CreateModel(
            name='User_Up',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('up_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.up')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
        migrations.CreateModel(
            name='Up_Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('up_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.up')),
                ('video_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.video')),
            ],
        ),
    ]
