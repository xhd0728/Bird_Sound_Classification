from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.models import User
from user.serializers import UserSerializer
from pkg.auth.code import send_code, check_code

from django.contrib.auth import login


class EmailView(APIView):
    def post(self, request):
        email = request.data.get("email")
        ok, msg = send_code(email)
        if not ok:
            return Response({"detail": msg}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        code = request.data.get("code")
        if not check_code(email, code):
            return Response({"detail": "邮箱验证不通过"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username):
            return Response({"detail": "用户名已被使用"}, status=status.HTTP_400_BAD_REQUEST)
        elif User.objects.filter(email=email):
            return Response({"detail": "邮箱已被使用"}, status=status.HTTP_400_BAD_REQUEST)
        User.objects.create_user(
            username=username, password=password, email=email, level_id=2)
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)


class UsersView(APIView):
    """登录模块(cookie)"""

    def post(self, request):
        username_or_email = request.data.get("username")
        password = request.data.get("password")
        if not username_or_email or not password:
            return Response({"detail": "账号或密码缺失"}, status=status.HTTP_400_BAD_REQUEST)
        user: User = User.objects.filter(username=username_or_email).first()
        if not user:
            user = User.objects.filter(email=username_or_email).first()
        if not user or not user.check_password(password):
            return Response({"detail": "账号或密码错误"}, status=status.HTTP_400_BAD_REQUEST)
        login(request, user)
        return Response({"detail": "登录成功", "user": UserSerializer(user).data})
