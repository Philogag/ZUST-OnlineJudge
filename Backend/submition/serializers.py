from rest_framework import serializers

from .models import Submition

class SubmitionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submition
        # fields = '__all__'
        exclude = ['code', 'statue_detail', 'judger_msg']

class SubmitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submition
        fields = '__all__'

class SubmitionJQSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submition
        fields = [
            'id',
            'pid',
            'contestid',
            'lang',
            'code',
        ]