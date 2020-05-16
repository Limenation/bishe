#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.urls import path

from .views import RegisterView, LoginView, RegisterActiveView, UserInfoView, ForgetpwdView, PwdresetView, \
    PwdmodifyView, LogoutView, MyCourseView, MyfavOrgView, MyfavCourseView, MyfavTeacherView, MyMessageView, \
    UploadImageView, UploadPwdView, UploadUserInfoView, UpdateEmailView

urlpatterns = [
    # 用户注册
    path('register/', RegisterView.as_view(), name='register'),
    # 用户登录
    path('login/', LoginView.as_view(), name='login'),
    # 注册激活链接
    path('active/<url_active_code>/', RegisterActiveView.as_view()),
    # 个人中心
    path('userinfo/', UserInfoView.as_view(), name='userinfo'),
    # 个人中心——头像修改
    path('uploadimage/', UploadImageView.as_view(), name='uploadimage'),
    # 个人中心——密码修改
    path('uploadpwd/', UploadPwdView.as_view(), name='uploadpwd'),
    # 个人中心——基本资料修改
    path('uploadinfo/', UploadUserInfoView.as_view(), name='uploadinfo'),
    # 个人中心-修改邮箱
    path('update_email/', UpdateEmailView.as_view(), name='update_email'),
    # 我的课程
    path('mycourse/', MyCourseView.as_view(), name='mycourse'),
    # 我的收藏——机构
    path('myfavorg/', MyfavOrgView.as_view(), name='myfavorg'),
    # 我的收藏——课程
    path('myfavcourse/', MyfavCourseView.as_view(), name='myfavcourse'),
    # 我的收藏——教师
    path('myfavteacher/', MyfavTeacherView.as_view(), name='myfavteacher'),
    # 我的消息
    path('mymessage/', MyMessageView.as_view(), name='mymessage'),
    # 忘记密码
    path('forgetpwd/', ForgetpwdView.as_view(), name='forgetpwd'),
    # 重置密码链接
    path('pwdreset/<url_pwdreset_code>/', PwdresetView.as_view(), name='pwdreset'),
    # 重置密码处理
    path('pwdmodify/', PwdmodifyView.as_view(), name='pwdmodify'),
    # 注销登录/登出
    path('logout/', LogoutView.as_view(), name='logout'),

]
