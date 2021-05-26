from django.core.mail import send_mail
from django.conf import settings

from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import (
    CreateModelMixin, RetrieveModelMixin,
    UpdateModelMixin, DestroyModelMixin,
    ListModelMixin)

import redis
import secrets
import json

from users.models import Supplier, Customer, User
from .serializers import (RegisterSupplierSerializer, RegisterCustomerSerializer,
                          UpdateSupplierSerializer, UpdateCustomerSerializer,
                          ChangePassswordSerializer, ResetPasswordSerializer,
                          SetPasswordSerializer)


class SupplierView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = Supplier.objects.filter(pk=self.request.user.pk)
        if user:
            return Supplier.objects.all()
        return Customer.objects.all()

    def get_object(self, *args, **kwargs):
        return self.get_queryset().get(pk=self.request.user.pk)

    def get_serializer_class(self):
        user = Supplier.objects.filter(pk=self.request.user.pk)
        if user:
            return UpdateSupplierSerializer
        else:
            return UpdateCustomerSerializer


class ChangePassowrd(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = ChangePassswordSerializer

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

class RegisterSupllierApiView(CreateAPIView):
    serializer_class = RegisterSupplierSerializer


class RegisterCustomerApiView(CreateAPIView):
    serializer_class = RegisterCustomerSerializer


class ResetPasswordApiView(APIView):
    serializer_class = ResetPasswordSerializer
    def post(self, request):
        serilizered_data = self.serializer_class(data=request.data)
        if serilizered_data.is_valid():
            r = redis.Redis(host='localhost', port=6379, db=0)
            token = secrets.token_urlsafe(16)
            email = serilizered_data.data['email']
            r.set(token, email, ex=60*40)
            message = f'for resetting your password send your new \
                 and confirm password with post method to \
                <a href="http://localhost:8000/user/set_password_api/{token}/">here</a>'

            send_mail(
                'ResetPassword',
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            r.close()
        return Response("Go and Check your email")


class SetPasswordApiView(APIView):
    serializer_class = SetPasswordSerializer

    def post(self, request, token):
        serilized_data = self.serializer_class(data=request.data)
        if serilized_data.is_valid():
            r = redis.Redis(host='localhost', port=6379, db=0)
            print(type(r.get(token)))
            mail = r.get(token).decode('utf-8')
            print(mail)
            user = User.objects.get(email=mail)
            print(serilized_data.validated_data['password1'])
            user.set_password(serilized_data.validated_data['password1'])
            user.save()
            return Response(serilized_data.validated_data, status=status.HTTP_200_OK)
        
        return Response(serilized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        
        