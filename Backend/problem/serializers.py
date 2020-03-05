from rest_framework import serializers

from .models import Problem

class ProblemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = [
            'id',
            'judge_method',
            'writer',
            'title',
            'tags',
            'show_level',
            'tot_cnt',
            'ac_cnt'
        ]

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'


class ProblemJQSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = [
            'judge_method',
            'real_pid',
            'time_limit',
            'mem_limit',
            'spj',
        ]