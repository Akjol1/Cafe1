from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token


from .permissoins import IsActivePermission
from .models import User
from .serializers import ChangePasswordSerializer, ForgotPasswordCompleteSerializer, ForgotPaswordSerializer, RegisterSerializer


from drf_yasg.utils import swagger_auto_schema


class RegisterView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer())
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                'Successufuly registered', 201
            )


class ActivationView(APIView):
    def get(self, request, email, activation_code):
        user = User.objects.filter(email=email, activation_code=activation_code).first()
        if not user:
            return Response(
                'User does not exist',
                400
            )
        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response(
            'Activated',
            200
        )
    
# class LoginView(ObtainAuthToken):
#     serializer_class = LoginSerializer



class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request':request})

        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()

        return Response('Status: 200. Пароль успешно обновлен')


class ForgotPasswordView(APIView):

    @swagger_auto_schema(request_body=ForgotPaswordSerializer)
    def post(self, request):
        serializer = ForgotPaswordSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.send_verification_email()

        return Response('Вам выслали сообщение для восстановления аккаунта')



class ForgotPasswordCompleteView(APIView):

    @swagger_auto_schema(request_body=ForgotPasswordCompleteSerializer)
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response('Пароль успешно изменён')
        

