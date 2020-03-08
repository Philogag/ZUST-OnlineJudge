from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

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

def submition_to_qdict(submition=None, data=None, problem=None):
    qsubmition = None
    if data != None:
        qsubmition = SubmitionJQSerializer(data=data)
        qsubmition.is_valid()
    else:
        qsubmition = SubmitionJQSerializer(submition)
    ret = qsubmition.data.copy()
    
    problem = problem
    if problem == None:
        problem = ProblemJQSerializer(
            Problem.objects.get(id=qsubmition.data["pid"])
        )
    ret.update(problem.data)
    return ret

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
                ret = submition_to_qdict(serializer.validated_data.copy())
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
        try:
            operator = request.GET.get('op')
            if operator == 'rejudge': # 重判
                uid = request.GET.get('id', default=None)
                if uid != None:
                    submition = Submition.objects.get(id=uid)
                    if submition.statue < 0:
                        return Statue(
                            status.HTTP_400_BAD_REQUEST,
                            'This submiton is already in judging'
                        ).to_JsonResponse()
                    RabbitMQ().put(
                        submition_to_qdict(submition)
                    )
                    return Statue(
                        status.HTTP_202_ACCEPTED,
                        'ok',
                    ).to_JsonResponse()
                else:
                    pid = request.GET.get('pid', default='*')
                    statue = request.GET.get('statue', default='*')
                    confirm = request.GET.get('confirm', default=0)
                    q = Q()
                    if pid != '*':
                        q = q & Q(pid=pid)
                    if statue != '*':
                        q = q & Q(statue=statue)
                    objs = Submition.objects.filter(q)

                    if confirm == 0:
                        return Statue(
                            status.HTTP_200_OK,
                            "{count:%d}" % objs.count()
                        ).to_JsonResponse()
                    else:
                        cnt = 0
                        for obj in objs:
                           # if obj.statue < 0:
                           #     continue
                            print(obj)
                            obj.statue = STATUE.WAITING
                            obj.save()
                            RabbitMQ().put(
                                submition_to_qdict(obj)
                            )
                            cnt += 1
                        return Statue(
                            status.HTTP_200_OK,
                            "{count:%d}" % cnt,
                        ).to_JsonResponse()

            elif operator == 'del': # 删除提交
                pass
        except BaseException as e:
            raise e
        return Statue(
            status.HTTP_403_FORBIDDEN,
            'You are NOT ALLOWED to use this page' 
        ).to_JsonResponse()

class JudgeAPI(APIView):
    def post(self, request):
        """
        测评机应答
        """
        if request.method == 'POST':
            data = request.data.copy()
            if data["judger-keygen"] == JUDGER_KEYGEN:
                submition = Submition.objects.get(id=data["id"])
                submition.statue = data["result"]
                submition.statue_detail = data["case"]
                submition.judger_msg = data["msg"]
                submition.max_mem_use_kb = data["max_mem_use_kb"]
                submition.max_time_use_ms = data["max_time_use_ms"]
                submition.save()
                return Statue(
                    status.HTTP_202_ACCEPTED, 'Accept.'
                ).to_JsonResponse()

            return Statue(
                status.HTTP_403_FORBIDDEN,
                'Judger keygen error!'
            ).to_JsonResponse()

        return Statue(
            status.HTTP_403_FORBIDDEN,
            'You are NOT ALLOWED to use this page' 
        ).to_JsonResponse()

