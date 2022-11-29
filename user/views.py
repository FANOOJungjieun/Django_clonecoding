import os
from uuid import uuid4
from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from .models import User
from jinstagram.settings import MEDIA_ROOT

class Join(APIView):
    def get(self, request):
        return render(request, 'user/join.html')

    def post(self, request):
        password = request.data.get('password')
        email = request.data.get('email')
        user_id = request.data.get('user_id')
        name = request.data.get('name')

        # make_password(password)
        User.objects.create(password=make_password(password),
                            email=email,
                            user_id=user_id,
                            name=name)
        return Response(status=200)

class Login(APIView):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        # 로그인
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = User.objects.filter(email=email).first()
        if user is None:
            return Response(status=400, data=dict(message="회원정보가 잘못되었습니다."))

        if user.check_password(password):
            request.session['email'] = email
            return Response(status=200, data=dict(message='로그인에 성공했습니다.'))
        else:
            return Response(status=400, data=dict(message="회원정보가 잘못되었습니다."))


class LogOut(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, 'user/login.html')

class UpdateProfile(APIView):
    def post(self, request):
        email = request.session.get('email', None)
        if email is None:
            return render(request, 'user/login.html')

        user = User.objects.filter(email=email).first()
        if user is None:
            return render(request, 'user/login.html')

        file = request.FILES['file']
        if file is None:
            return Response(status=500)

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        user.thumbnail = uuid_name
        user.save()

        return Response(status=200, data=dict(uuid=uuid_name))