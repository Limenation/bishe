# _*_ coding:utf-8 _*_
import json

from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from pure_pagination import Paginator, PageNotAnInteger  # 实现分页功能
from django.urls import reverse

from .forms import RegisterForm, LoginForm, ForgetpwdForm, PwdmodifyForm, UpImageForm, UpUserInfoForm
from .models import UserProfile, EmailVerification, Banner
from utils.email_send import send_link_email
from operation.models import UserCourse, UserFav, UserMessage
from organizations.models import Organizationinfo, Teacher
from courses.models import Courseinfo
from utils.mixin_utils import LoginRequiredMixin

from django.utils.decorators import method_decorator
from django.contrib.auth.views import method_decorator


class IndexView(View):
    """显示首页"""

    def get(self, request):
        banners = Banner.objects.all().order_by('-order')[:3]
        courses = Courseinfo.objects.all().order_by('-click_nums')[:6]
        orgs = Organizationinfo.objects.all().order_by('click_nums').order_by('-course_nums')[:15]
        banner_courses = Courseinfo.objects.filter(is_banner=True).order_by('-click_nums')[:3]

        return render(request, 'index.html', {
            'banners': banners,
            'courses': courses,
            'orgs': orgs,
            'banner_courses': banner_courses,
        })


class RegisterView(View):
    """用户注册功能"""

    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            if UserProfile.objects.filter(email=email):  # 判断邮箱是否已经注册过了
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已经存在！'})
            else:
                user_profile = UserProfile()
                user_profile.username = email
                user_profile.email = email
                user_profile.password = make_password(password)
                user_profile.is_active = False
                user_profile.save()

                try:
                    send_link_email(email)  # 发送激活邮件
                except AttributeError:
                    return render(request, 'register.html', {'msg': '邮箱错误'})
                return render(request, "email_send_success.html", {'email': email, 'msg': '请前往查收并尽快激活账户'})

        else:
            return render(request, 'register.html', {'register_form': register_form})


class RegisterActiveView(View):
    """注册激活功能"""

    def get(self, request, url_active_code):
        regis_actives = EmailVerification.objects.filter(code=url_active_code, is_delete=0)
        if regis_actives:
            for regis_active in regis_actives:
                email = regis_active.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()

                regis_active.is_delete = 1
                regis_active.save()
                return render(request, 'register_active_sucessed.html', {})
        else:
            return render(request, 'register_active_failed.html', {})


class ChongxieAuthenticate(ModelBackend):
    """重写authenticate方法,使之可以对邮箱验证"""

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
            else:
                return None
        except Exception as e:
            return None


class LoginView(View):
    """用户登录功能"""

    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login_user = request.POST.get('username', '')
            login_password = request.POST.get('password', '')
            user = authenticate(username=login_user, password=login_password)
            if user:  # 通过验证
                if user.is_active:  # 已激活
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'login_form': login_form, 'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class ForgetpwdView(View):
    """登录页面点击忘记密码"""

    def get(self, request):
        forgetpwd_form = ForgetpwdForm()
        return render(request, 'forgetpwd.html', {'forgetpwd_form': forgetpwd_form})

    def post(self, request):
        """获取邮箱并发送重置密码链接"""
        forgetpwd_form = ForgetpwdForm(request.POST)
        if forgetpwd_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):
                try:
                    send_link_email(email, send_type='forget')  # 发送重置密码链接
                except AttributeError:
                    return render(request, 'forgetpwd.html', {'msg': '邮箱错误'})
                return render(request, "email_send_success.html", {'email': email, 'msg': '请前往查收并点击链接重置密码'})
            else:
                return render(request, 'forgetpwd.html', {'forgetpwd_form': forgetpwd_form, 'msg': '该邮箱未注册'})
        else:
            return render(request, 'forgetpwd.html', {'forgetpwd_form': forgetpwd_form})


class PwdresetView(View):
    """密码重置链接处理,点击转向密码重置页面"""

    def get(self, request, url_pwdreset_code):
        pwdreset_code = url_pwdreset_code
        users = EmailVerification.objects.filter(code=pwdreset_code, is_delete=0)
        if users:
            for user in users:
                email = user.email
                return render(request, 'password_reset.html', {'email': email, 'pwdreset_code': pwdreset_code})
        else:
            return render(request, 'register_active_failed.html')


class PwdmodifyView(View):
    """密码重置功能"""

    def post(self, request):
        """密码重置处理"""
        pwdmodify_form = PwdmodifyForm(request.POST)
        if pwdmodify_form.is_valid():
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            pwdmodify_email = request.POST.get('email', '')
            pwdmodify_code = request.POST.get('pwdreset_code', '')
            if password1 == password2:
                pwdmodify_user = UserProfile.objects.get(email=pwdmodify_email)
                pwdmodify_user.password = make_password(password1)
                pwdmodify_user.save()

                pwdmodify_code_es = EmailVerification.objects.filter(code=pwdmodify_code)
                for pwdmodify_code_e in pwdmodify_code_es:
                    pwdmodify_code_e.is_delete = 1
                    pwdmodify_code_e.save()

                    return render(request, 'login.html', {'pwdreset_msg': '密码重置成功，请登录'})
            else:
                return render(request, 'password_reset.html',
                              {'pwdmodify_form': pwdmodify_form, 'msg': '两次输入不一致，请重新输入'})
        else:
            return render(request, 'password_reset.html', {'pwdmodify_form': pwdmodify_form})


class LogoutView(View):
    """注销登录功能"""

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class UserInfoView(View):
    """用户的个人中心"""

    def get(self, request):
        """进入个人中心"""
        user = request.user.username
        if not user:  # 未登录
            return render(request, 'login.html', {'pwdreset_msg': '您还未登录...'})
        else:
            return render(request, 'usercenter-info.html')


class MyCourseView(LoginRequiredMixin, View):
    """个人中心之我的课程"""

    def get(self, request):
        user_id = request.user.id
        courses = UserCourse.objects.filter(user_id=user_id)
        return render(request, 'usercenter-mycourse.html', {
            'courses': courses,
        })


class MyfavCourseView(LoginRequiredMixin, View):
    """个人中心之我收藏的课程"""

    def get(self, request):
        user_id = request.user.id
        fav_ids = [userfav.fav_id for userfav in UserFav.objects.filter(user_id=user_id, fav_type=0)]
        courses = Courseinfo.objects.filter(id__in=fav_ids)
        return render(request, 'usercenter-fav-course.html', {
            'courses': courses,

        })


class MyfavOrgView(LoginRequiredMixin, View):
    """个人中心之我收藏的机构"""

    def get(self, request):
        user_id = request.user.id
        fav_ids = [userfav.fav_id for userfav in UserFav.objects.filter(user_id=user_id, fav_type=1)]
        orgs = Organizationinfo.objects.filter(id__in=fav_ids)
        return render(request, 'usercenter-fav-org.html', {
            'orgs': orgs,

        })


class MyfavTeacherView(LoginRequiredMixin, View):
    """个人中心之我收藏的教师"""

    def get(self, request):
        user_id = request.user.id
        fav_ids = [userfav.fav_id for userfav in UserFav.objects.filter(user_id=user_id, fav_type=2)]
        teachers = Teacher.objects.filter(id__in=fav_ids)
        return render(request, 'usercenter-fav-teacher.html', {
            'teachers': teachers,
        })


class MyMessageView(LoginRequiredMixin, View):
    """个人中心之我的消息"""

    def get(self, request):
        user_id = request.user.id
        messages = UserMessage.objects.filter(Q(user_id=user_id) | Q(user_id=0))

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(messages, 5, request=request)
        messagess = p.page(page)

        return render(request, 'usercenter-message.html', {
            'messages': messagess,
        })


class UploadImageView(LoginRequiredMixin, View):
    """个人中心头像修改"""

    def post(self, request):
        uploadimage_forms = UpImageForm(request.POST, request.FILES, instance=request.user)
        res = dict()
        if uploadimage_forms.is_valid():
            uploadimage_forms.save()
            res['status'] = 'success'
            res['msg'] = '头像修改成功'
        else:
            res['status'] = 'fail'
            res['msg'] = '头像修改失败'
        return HttpResponse(json.dumps(res), content_type='application/json')


class UploadPwdView(LoginRequiredMixin, View):
    """个人中心的密码修改"""

    def post(self, request):
        pwdmodify_form = PwdmodifyForm(request.POST)
        res = dict()
        if pwdmodify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                res['status'] = 'fail'
                res['msg'] = '两次密码不一致'
                return HttpResponse(json.dumps(res), content_type='application/json')

            user = request.user
            user.password = make_password(pwd2)
            user.save()

            res['status'] = 'success'
            res['msg'] = '密码修改成功'
        else:
            res = pwdmodify_form.errors
        return HttpResponse(json.dumps(res), content_type='application/json')


class UploadUserInfoView(LoginRequiredMixin, View):
    """个人中心的个人资料修改"""

    def post(self, request):
        user_form = UpUserInfoForm(request.POST, instance=request.user)
        res = dict()
        if user_form.is_valid():
            user = UserProfile.objects.get(id=request.user.id)
            user.nick_name = request.POST.get('nick_name', '')
            user.birthday = request.POST.get('birthday', '')
            user.gender = request.POST.get('gender', '')
            user.address = request.POST.get('address', '')
            user.mobile = request.POST.get('mobile', '')
            user.save()

            res['status'] = 'success'
        else:
            res = user_form.errors
        return HttpResponse(json.dumps(res), content_type='application/json')


class UpdateEmailView(View):
    """个人中心的邮箱修改"""

    def get(self, request):
        email = request.GET.get('email', '')
        res = dict()
        # res['status'] = 'success'
        if not email:
            res['status'] = 'failure'
            return HttpResponse(json.dumps(res), content_type='application/json')
        try:
            send_link_email(email, send_type='update_email')  # 发送邮箱验证码
            res['status'] = 'success'
            return HttpResponse(json.dumps(res), content_type='application/json')
        except BaseException as e:
            res['status'] = 'failure'
            return HttpResponse(json.dumps(res), content_type='application/json')

    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        user = request.user
        user_ = EmailVerification.objects.filter(code=code, is_delete=0)
        res = dict()
        if email and code and user_ and user:
            user_[0].is_delete = 1
            user_[0].save()
            user.email = email
            user.save()

            res['status'] = 'success'
            return HttpResponse(json.dumps(res), content_type='application/json')
        res['status'] = 'failure'
        return HttpResponse(json.dumps(res), content_type='application/json')


def page_not_look(request):
    """全局403配置"""
    from django.shortcuts import render_to_response
    response = render_to_response('403.html', {})
    response.status_code = 403
    return response


def page_not_found(request):
    """全局404配置"""
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    """全局500配置"""
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
