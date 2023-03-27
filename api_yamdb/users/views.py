from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework import filters, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from .serializers import (TokenSerializer, UserSerializer,
                          RegisterDataSerializer, AdminSerializer)
from .permissions import IsAdmin


class AdminAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )
    http_method_names = ['get', 'post', 'list', 'patch', 'delete']


class UserMePatchView(APIView):

    def get(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response('Вы не авторизованы',
                        status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response('Вы не авторизованы',
                        status=status.HTTP_401_UNAUTHORIZED)


class RegistrationAPI(APIView):
    """Аутентификация через верификацию email"""
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = RegisterDataSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email']).exists():
            user = get_object_or_404(
                User,
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'])
        else:
            serializer.save()
            user = get_object_or_404(
                User, username=serializer.validated_data['username'])
        confirmation_code = default_token_generator.make_token(user)
        send_mail('Подтверждение регистрации',
                  f'Подтвердите ваш e-mail: {confirmation_code}',
                  DEFAULT_FROM_EMAIL, [serializer.data['email']],
                  fail_silently=False)
        return Response(serializer.data, status.HTTP_200_OK)


class TokenAPI(APIView):

    permission_classes = (AllowAny, )
    serializer_class = TokenSerializer

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=serializer.data['username'])

        if default_token_generator.check_token(
                user, serializer.validated_data["confirmation_code"]):
            token = AccessToken.for_user(user)
            return Response({"token": str(token)}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
