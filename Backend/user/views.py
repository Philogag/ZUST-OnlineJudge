from django.http import HttpResponse, JsonResponse

from rest_framework.views import APIView
from rest_framework import status

from statue_api import Statue
from .serializers import UserSerializer, UserAuthOnlySerializer
from .models import User, USER_LEVEL


def get(request, action):
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


class UserView(APIView):
    @staticmethod
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
