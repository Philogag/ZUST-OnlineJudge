from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status

from datetime import datetime

from statue_api import Statue

from .models import Problem, JUDGE_METHOD
from .serializers import ProblemSerializer, ProblemListSerializer

class ProblemAllView(APIView):
    def get(self, request):
        """
        题库
        """
        problems = Problem.objects.all()
        serializer = ProblemListSerializer(problems, many=True)
        return JsonResponse(serializer.data, safe=False)

class ProblemView(APIView):
    def get(self, request, ID):
        """
        题目
        """
        serializer = None
        try:
            submition = Problem.objects.get(id=ID)
            serializer = ProblemSerializer(submition)
            return JsonResponse(serializer.data, safe=False)
        except BaseException:
            return Statue(
                status.HTTP_404_NOT_FOUND,
                'Problem not found'
            ).to_JsonResponse()

    def post(self, request):
        """
        新建题目
        """
        data = request.data.copy()
        if int(data["judge_method"]) == int(JUDGE_METHOD.Local):
            data["real_pid"] = -1
        data["last_edit"] = datetime.timestamp(datetime.now())
        serializer = ProblemSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            
            return JsonResponse(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        
        return Statue(
            status.HTTP_400_BAD_REQUEST,
            serializer.errors
        ).to_JsonResponse()
                
