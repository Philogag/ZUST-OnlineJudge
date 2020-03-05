from django.http import JsonResponse

from rest_framework import status

class Statue():
    def __init__(self, code, detial = ""):
        self.code = code
        self.detial = detial
    
    def to_JsonResponse(self):
        return JsonResponse(
            {'code': self.code, 'detial': self.detial},
            status=self.code
        )