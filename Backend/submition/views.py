from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status

from datetime import datetime

from Backend.settings import JUDGER_KEYGEN
from problem.models import Problem
from problem.serializers import ProblemJQSerializer
from rabbitmq import RabbitMQ
from statue_api import Statue

from .serializers import SubmitionSerializer, SubmitionListSerializer,SubmitionJQSerializer
from .models import Submition, STATUE


class SubmitionALLView(APIView):
    def get(self, request):
        """
        提交列表
        """
        submitions = Submition.objects.all()
        serializer = SubmitionListSerializer(submitions, many=True)
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
            return Statue(
                status.HTTP_404_NOT_FOUND,
                'Submition not found'
            ).to_JsonResponse()

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
                qsubmition = SubmitionJQSerializer(data=serializer.validated_data)
                if not qsubmition.is_valid():
                    return Statue(
                        status.HTTP_500_INTERNAL_SERVER_ERROR,
                        "Error at line 65:\n" + qsubmition.errors
                    ) 
                ret = qsubmition.data.copy()
                
                problem = ProblemJQSerializer(
                    Problem.objects.get(id=qsubmition.data["pid"])
                )
                ret.update(problem.data)
                serializer.save()
                ret['id'] = serializer.data['id']
                RabbitMQ().put(ret)
                return JsonResponse(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            except BaseException as e:
                raise e
                return Statue(
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "Error at line 81:\n" + str(e)
                ).to_JsonResponse()

        return Statue(
            status.HTTP_400_BAD_REQUEST,
            "Error at line 86:\n" + serializer.errors
        ).to_JsonResponse()

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
                return Statue(
                    status.HTTP_202_ACCEPTED
                ).to_JsonResponse()

            return Statue(
                status.HTTP_403_FORBIDDEN,
                'Judger keygen error!'
            ).to_JsonResponse()

        return Statue(
            status.HTTP_403_FORBIDDEN,
            'You are NOT ALLOWED to use this page' 
        ).to_JsonResponse()

