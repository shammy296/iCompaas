from knox import views
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.exceptions import ValidationError, AuthenticationFailed
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
                user = User.objects.get(contact=request.data.get('phone'))
            else:
                user = User.objects.get(email=request.data.get('email'))

            if authenticate(username=user.username, password=request.data.get('password')):
                request.user = user
                return super(LoginView, self).post(request, *args, **kwargs)

            raise AuthenticationFailed({'msg': 'User/Password does not match.'})

        except ObjectDoesNotExist:
            raise ValidationError({'msg': 'User not found.'})


class UserInfoView(APIView):
    model_object = User.objects
    serializer_class = UserInfoSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            queryset = self.model_object.filter(id=request.GET.get('id'))
            return Response(self.serializer_class(queryset, many=True).data)
        except ObjectDoesNotExist:
            raise ValidationError({'msg': 'User not found.'})

    def put(self, request, **kwargs):
        # queryset = self.model_object.filter(id=request.GET.get('id'))
        # return Response(self.serializer_class(queryset, many=True).data)
        raise ValidationError('WIP')

    def delete(self, request, **kwargs):
        try:
            instance = self.model_object.filter(id=kwargs.get('pk'))
            if not instance.is_superuser and request.user != instance:
                raise ValidationError({'msg': 'Not authorize to delete user.'})
            instance.delete()
            return Response({'msg': 'User Deleted.'}, status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            raise ValidationError({'msg': 'User not found.'})


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        raise ValidationError('WIP')


class ResetPasswordView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        raise ValidationError('WIP')
