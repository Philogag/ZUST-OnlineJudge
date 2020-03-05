from rest_framework import serializers

from .models import Problem

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        field = '__all__'

class ProblemJQSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        field = [
            'judge_method',
            'real_pid',
            'time_limit',
            'mem_limit',
            'spj',
        ]