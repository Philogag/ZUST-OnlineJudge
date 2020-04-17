from datetime import datetime

from django.db.models import Q
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from Backend.settings import JUDGER_KEYGEN
from problem.models import Problem
from problem.serializers import ProblemJQSerializer
from rabbitmq import RabbitMQ
from statue_api import Statue
from .models import Submission, STATUE
from .serializers import SubmissionSerializer, SubmissionListSerializer, SubmissionJQSerializer


def submission_to_qdict(submission=None, data=None, problem=None):
    qsubmission = None
    if data is not None:
        qsubmission = SubmissionJQSerializer(data=data)
        qsubmission.is_valid()
    else:
        qsubmission = SubmissionJQSerializer(submission)
    ret = qsubmission.data.copy()

    problem = problem
    if problem is None:
        problem = ProblemJQSerializer(
            Problem.objects.get(id=qsubmission.data["pid"])
        )
    ret.update(problem.data)
    return ret


class SubmissionALLView(APIView):
    @staticmethod
    def get(request):
        """
        提交列表
        """
        submissions = Submission.objects.all()
        serializer = SubmissionListSerializer(submissions, many=True)
        return JsonResponse(serializer.data, safe=False)


class SubmissionView(APIView):
    @staticmethod
    def get(self, request, sid):  # 查询
        """
        单个提交
        """
        serializer = None
        # noinspection PyBroadException
        try:
            submission = Submission.objects.get(id=sid)
            serializer = SubmissionSerializer(submission)
            return JsonResponse(serializer.data, safe=False)
        except BaseException:
            return Statue(
                status.HTTP_404_NOT_FOUND,
                'Submission not found'
            ).to_JsonResponse()

    @staticmethod
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
        serializer = SubmissionSerializer(data=data)
        if serializer.is_valid():

            try:
                ret = submission_to_qdict(serializer.validated_data.copy())
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
            status.HTTP_400_BAD_REQUEST,
            "Error at line 86:\n" + serializer.errors
        ).to_JsonResponse()


class AdminAPI(APIView):
    @staticmethod
    def get(self, request):
        """
        管理员操作接口
        功能: 1.重判 2.删除提交
        """
        try:
            operator = request.GET.get('op')
            if operator == 'rejudge':  # 重判
                uid = request.GET.get('id', default=None)
                if uid is not None:
                    submission = Submission.objects.get(id=uid)
                    if submission.statue < 0:
                        return Statue(
                            status.HTTP_400_BAD_REQUEST,
                            'This submission is already in judging'
                        ).to_JsonResponse()
                    RabbitMQ().put(
                        submission_to_qdict(submission)
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
                    objs = Submission.objects.filter(q)

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
                                submission_to_qdict(obj)
                            )
                            cnt += 1
                        return Statue(
                            status.HTTP_200_OK,
                            "{count:%d}" % cnt,
                        ).to_JsonResponse()

            elif operator == 'del':  # 删除提交
                pass
        except BaseException as e:
            raise e
        return Statue(
            status.HTTP_403_FORBIDDEN,
            'You are NOT ALLOWED to use this page'
        ).to_JsonResponse()


class JudgeAPI(APIView):
    @staticmethod
    def post(self, request):
        """
        测评机应答
        """
        if request.method == 'POST':
            data = request.data.copy()
            if data["judger-keygen"] == JUDGER_KEYGEN:
                submition = Submission.objects.get(id=data["id"])
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
