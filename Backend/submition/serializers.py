from rest_framework import serializers

from .models import Submition

class SubmitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submition
        fields = '__all__'

class SubmitionJQSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submition
        fields = [
            'judge_method',
            'pid',
            'contestid',
            'lang',
            'code',
        ]