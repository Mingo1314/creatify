from django.shortcuts import render

# Create your views here.

from rest_framework.permissions import AllowAny
from django.conf import settings
from django.db import transaction
from django.utils import timezone

from common.cache import set_jwt_token, check_login
from common.utils import check_email, check_password
from common.views import CreatifyView
from users.models import User
from exceptions import excptions as exc


class SignUpView(CreatifyView):
    """
    用户注册
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        email = check_email(request.data.get('email', ""))
        password = check_password(request.data.get('password', ""))

        if not email:
            raise exc.EmailFormatException()
        if not password:
            raise exc.PasswordFormatException()

        with transaction.atomic():
            if User.objects.filter(email=email).exists():
                raise exc.EmailExistException()
            user = User.objects.create_user('username', password=password, email=email)
            return {
                "id": user.id,
                "email": user.email
            }


class SignInView(CreatifyView):
    """
    用户登录
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        email = check_email(request.data.get('email', ""))
        password = request.data.get('password', "")
        if not email:
            raise exc.EmailFormatException()
        if not password:
            raise exc.PasswordFormatException()

        with transaction.atomic():
            user = User.objects.filter(email=email).first()
            if not user:
                raise exc.AuthenticationException()
            if not user.check_password(password):
                # TODO 密码失败次数处理
                raise exc.AuthenticationException()

            # TODO 检测并清零登录密码错误次数
            request.user = user
            tokens = set_jwt_token(user.id, email)
            request._SET_COOKIE = tokens["access_token"][0]
            return {k: v[0] for k, v in tokens.items()}


class MeView(CreatifyView):
    """
    用户登录确认
    """
    permission_classes = (AllowAny,)

    def get(self, request):
        jwt = request.META.get("HTTP_AUTHORIZATION", "")
        if not jwt:
            raise exc.NotLoginException()
        jwt = jwt[7:]
        user_id = check_login(jwt)
        if not user_id:
            raise exc.NotLoginException()
        user = User.objects.get(id=user_id)
        return {"user_id": user.id, "email": user.email}





