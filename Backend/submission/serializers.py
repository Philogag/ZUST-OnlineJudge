from rest_framework import serializers

from .models import Submission


class SubmissionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        # fields = '__all__'
        exclude = ['code', 'statue_detail', 'judger_msg']


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'


class SubmissionJQSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = [
            'id',
            'pid',
            'lang',
            'code',
        ]
