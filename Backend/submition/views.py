from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime

from Backend.settings import JUDGER_KEYGEN
from problem.models import Problem
from problem.serializers import ProblemJQSerializer
from rabbitmq import RabbitMQ

from .serializers import SubmitionSerializer, SubmitionJQSerializer
from .models import Submition, STATUE


def Submition_to_QueueData(submition):
    ret = SubmitionJQSerializer(data=submition).data.copy()
    try:
        problem = Problem.objects.get(id=ret["pid"])
        ret.append(ProblemJQSerializer(problem).data())
        print(ret)
        return ret


class SubmitionsView(APIView):
    def get(self, request):
        """
        提交列表
        """
        submitions = Submition.objects.all()
        serializer = SubmitionSerializer(submitions, many=True)
        return JsonResponse(serializer.data, safe=False)
    

class SubmitionView(APIView):
    
    def get(self, request, ID):  # 查询
        """
        单个提交
        """
        serializer = None
        try:
            submition = Submition.objects.get(id=ID)
            serializer = SubmitionSerializer(submition)
            return JsonResponse(serializer.data, safe=False)
        except BaseException:
            return JsonResponse(
                {'error':404, 'detials':'Submition not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request):
        """
        新提交
        """
        data = request.data.copy()
        data["statue"] = int(STATUE.WAITING)
        data["judger"] = ""
        data["statue_detail"] = ""
        data["judger_msg"] = ""
        data["timestamp"] = datetime.timestamp(datetime.now())
        serializer = SubmitionSerializer(data=data)
        if serializer.is_valid():
            
            try:
                data = Submition_to_QueueData(serializer.data)
                serializer.save()
                RabbitMQ().put(data)
                return JsonResponse(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            except BaseException as e:
                return JsonResponse(
                    {"code":500, "detial": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return JsonResponse(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class AdminAPI(APIView):
    def get(self, request):
        """
        管理员操作接口
        功能: 1.重判 2.删除提交
        """
        pass # TODO

class JudgeAPI(APIView):
    def post(self, request):
        """
        测评机应答
        """
        if request.method == 'POST':
            data = request.data
            if data["judger-keygen"] == JUDGER_KEYGEN:
                submition = Submition.objects.get(id=data["submitId"])
                submition.statue = data["result"]
                if data["result"] == STATUE.SYSTEM_ERROR \
                    or data["result"] == STATUE.COMPILE_ERROR:
                    submition.statue_detail = ""
                else:
                    submition.statue_detail = data["case"]
                submition.judger_msg = data["msg"]
                submition.save()
                return JsonResponse(
                    {"code": 202},
                    status=status.HTTP_202_ACCEPTED
                )
            return JsonResponse(
                {'code': 403, 'detials': 'Judger keygen error!'},
                statue=status.HTTP_403_FORBIDDEN
            )
        return JsonResponse(
            {'code':403, 'detials':'You are NOT ALLOWED to use this page'}, 
            status=status.HTTP_403_FORBIDDEN
        )

