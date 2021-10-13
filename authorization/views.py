from django.contrib.auth.models import Group
from knox import views
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.exceptions import ValidationError, AuthenticationFailed, PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authorization.models import User
from authorization.serializers import UserInfoSerializer


class LoginView(views.LoginView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            if request.data.get('username'):
                user = User.objects.get(username=request.data.get('username'))
            elif request.data.get('phone'):
                user = User.objects.get(phone=request.data.get('phone'))
            else:
                user = User.objects.get(email=request.data.get('email'))

            if authenticate(username=user.username, password=request.data.get('password')):
                request.user = user
                return super(LoginView, self).post(request, *args, **kwargs)

            raise AuthenticationFailed({'msg': 'Username/Password does not match.'})

        except ObjectDoesNotExist:
            raise ValidationError({'msg': 'User not found.'})


class UserInfoView(APIView):
    model_object = User.objects
    serializer_class = UserInfoSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            if request.GET.get('child'):
                queryset = self.model_object.filter(report_to=request.user)
                return Response(self.serializer_class(queryset, many=True).data)

            instance = self.model_object.get(username=request.user.username)

            return Response(self.serializer_class(instance).data)

        except ObjectDoesNotExist:
            raise ValidationError({'msg': 'User not found.'})

    def post(self, request):
        try:
            if self.model_object.filter(username=request.data.get('username')).exists():
                raise ValidationError('Username already used.')

            if self.model_object.filter(email=request.data.get('email')).exists():
                raise ValidationError('Email already used.')

            if self.model_object.filter(phone=request.data.get('phone')).exists():
                raise ValidationError('Phone already used.')

            instance = self.model_object.create_user(request.data.get('username'), request.data.get('email'), request.data.get('password'))
            instance.first_name = request.data.get('first_name')
            instance.last_name = request.data.get('last_name')
            instance.phone = request.data.get('phone')
            instance.report_to = request.user
            instance.save()

            return Response({'msg': 'User created.'}, status=status.HTTP_204_NO_CONTENT)

        except ValueError:
            raise ValueError({'msg': 'Username, email, password are mandatory fields.'})

    def put(self, request, **kwargs):
        try:
            instance = self.model_object.get(username=request.user.username)
            update_keys = request.data.keys()

            if 'username' in update_keys:
                if self.model_object.filter(username=request.data.get('username')).exists():
                    raise ValidationError({'msg': 'Username already used.'})
                instance.username = request.data.get('username')

            if 'first_name' in update_keys:
                instance.first_name = request.data.get('first_name')

            if 'last_name' in update_keys:
                instance.last_name = request.data.get('last_name')

            if 'is_active' in update_keys:
                if request.user != instance.report_to and request.user != instance:
                    raise PermissionDenied({'msg': 'You are not authorized to perform this action.'})
                instance.is_active = request.data.get('is_active')

            if request.data.get('report_to'):
                if request.user != instance.report_to:
                    raise PermissionDenied({'msg': 'You are not authorized to perform this action.'})
                instance.report_to = self.model_object.get(id=request.data.get('report_to'))

            if 'groups' in update_keys:
                instance.groups.clear()
                if request.data.get('groups'):
                    instance.groups.add(*[Group.objects.filter(id__in=request.data.get('groups'))])

            if 'phone' in update_keys:
                if self.model_object.filter(phone=request.data.get('phone')).exists():
                    raise ValidationError({'msg': 'Phone already used.'})
                instance.phone = request.data.get('phone')

            if 'password' in update_keys:
                if authenticate(username=instance.username, password=request.data.get('old_password')):
                    instance.set_password(request.data.get('password'))
                else:
                    raise ValidationError({'msg': 'Wrong password.'})

            instance.save()
            return Response(self.serializer_class(instance).data)

        except ObjectDoesNotExist:
            raise ValidationError({'msg': 'User not found.'})

    def delete(self, request, **kwargs):
        try:
            instance = self.model_object.get(id=kwargs.get('pk'))
            if not instance.is_superuser and request.user != instance:
                raise ValidationError({'msg': 'Not authorized to delete user.'})

            instance.delete()
            return Response({'msg': 'User Deleted.'}, status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            raise ValidationError({'msg': 'User not found.'})


class RegisterView(APIView):
    model_object = User.objects
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            if self.model_object.filter(username=request.data.get('username')).exists():
                raise ValidationError('Username already used.')

            if self.model_object.filter(email=request.data.get('email')).exists():
                raise ValidationError('Email already used.')

            if self.model_object.filter(phone=request.data.get('phone')).exists():
                raise ValidationError('Phone already used.')

            instance = self.model_object.create_user(request.data.get('username'), request.data.get('email'), request.data.get('password'))
            instance.first_name = request.data.get('first_name')
            instance.last_name = request.data.get('last_name')
            instance.phone = request.data.get('phone')
            instance.save()

            return Response({'msg': 'User created.'}, status=status.HTTP_204_NO_CONTENT)

        except ValueError:
            raise ValueError({'msg': 'Username, email, password are mandatory fields.'})


class ResetPasswordView(APIView):
    model_object = User.objects
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            instance = self.model_object.get(email=request.data.get('email'))
            instance.set_password(request.data.get('password'))
            instance.save()
            return Response({'msg': 'Password changed successfully.'}, status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            raise ValidationError({'msg': 'User not found.'})
