# Generated by Django 2.0.6 on 2020-02-17 16:12

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='城市')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '城市',
                'verbose_name_plural': '城市',
            },
        ),
        migrations.CreateModel(
            name='Organizationinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('gx', '高校'), ('pxjg', '培训机构'), ('gr', '个人')], default='gx', max_length=20, verbose_name='机构类别')),
                ('name', models.CharField(default='', max_length=100, verbose_name='机构名称')),
                ('image', models.ImageField(upload_to='orgs/%Y/%m', verbose_name='机构logo')),
                ('students', models.IntegerField(default=0, verbose_name='学习人数')),
                ('address', models.CharField(default='', max_length=200, verbose_name='机构地址')),
                ('desc', models.TextField(default='', verbose_name='机构介绍')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('is_authentication', models.BooleanField(choices=[(0, '未认证'), (1, '已认证')], default=0, verbose_name='是否已认证')),
                ('is_gold', models.BooleanField(choices=[(0, '非金牌机构'), (1, '金牌机构')], default=0, verbose_name='是否为金牌机构')),
                ('course_nums', models.IntegerField(default=0, verbose_name='课程数')),
                ('tag', models.CharField(default='全国知名', max_length=20, verbose_name='机构标签')),
                ('click_nums', models.IntegerField(default=0, verbose_name='点击数')),
                ('fav_nums', models.IntegerField(default=0, verbose_name='收藏数')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.City', verbose_name='所在城市')),
            ],
            options={
                'verbose_name': '授课机构',
                'verbose_name_plural': '授课机构',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=20, verbose_name='姓名')),
                ('image', models.ImageField(default='default1.png', upload_to='teachers/%Y/%m', verbose_name='头像')),
                ('age', models.IntegerField(default=30, verbose_name='年龄')),
                ('work_years', models.IntegerField(default=0, verbose_name='工作年限')),
                ('work_position', models.CharField(default='', max_length=20, verbose_name='工作职位')),
                ('teach_points', models.CharField(default='', max_length=50, verbose_name='教学特点')),
                ('fav_nums', models.IntegerField(default=0, verbose_name='收藏数')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('is_authentication', models.BooleanField(choices=[(0, '未认证'), (1, '已认证')], default=0, verbose_name='是否已认证')),
                ('is_gold', models.BooleanField(choices=[(0, '非金牌教师'), (1, '金牌教师')], default=0, verbose_name='是否为金牌教师')),
                ('click_nums', models.IntegerField(default=0, verbose_name='点击数')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.Organizationinfo', verbose_name='就职单位')),
            ],
            options={
                'verbose_name': '教师',
                'verbose_name_plural': '教师',
            },
        ),
    ]