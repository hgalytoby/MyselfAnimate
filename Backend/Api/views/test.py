from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from Database.models import AnimateEpisodeInfoModel
from django.views import View


class TestView(APIView):
    def get(self, request):
        model = AnimateEpisodeInfoModel.objects.get(pk=1)
        a = model.ts_model.all()
        print(a)
        return Response({}, status=status.HTTP_200_OK)
