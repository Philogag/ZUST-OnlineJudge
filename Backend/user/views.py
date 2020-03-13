from django.http import HttpResponse, JsonResponse

from rest_framework.views import APIView
from rest_framework import status
from rest_framework_jwt.settings import api_settings

from datetime import datetime

from statue_api import Statue

from .serializers import UserSerializer, UserAuthOnlySerializer
from .models import User, USER_LEVEL

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

def generateToken(user):
    # 生成载荷信息(payload),根据user的信息生成一个payload
    payload = jwt_payload_handler(user)
    # 根据payload和secret_key，采用HS256，生成token.
    token = jwt_encode_handler(payload)
    user.token = token

def checkToken(token):
    pass
        

class UserView(APIView):
    def get(self, request, action):
        if action == 'login':
            username = request.GET.get('username')
            password = request.GET.get('password')
            try:
                user = User.objects.find(username=username)
                
                if not user.check_password(password):
                    return Statue(
                        status.HTTP_400_BAD_REQUEST,
                        'Password Wrong!'
                    ).to_JsonResponse()
                
                generateToken(user)
                user.save()

                return JsonResponse(
                    UserSerializer(user).data,
                    status=status.HTTP_200_OK
                )

            except User.REQUIRED_FIELDS:
                return Statue(
                    status.HTTP_400_BAD_REQUEST,
                    'User Not Found!',
                ).to_JsonResponse()

        return Statue(
            status.HTTP_404_NOT_FOUND,
        )
    
    def post(self, request, action):
        if action == 'set_password':
            pass

        if action == "create_user":
            pass
        
        if action == 'set_detail':
            pass

        return Statue(
            status.HTTP_404_NOT_FOUND,
        )
