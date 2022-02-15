from django.db.models import Prefetch, Model
from rest_framework.generics import ListAPIView


class BaseAnimateEpisodeDone(ListAPIView):
    animate_episode_info_model: Model
    animate_info_model: Model

    def list(self, request, *args, **kwargs):
        prefetch = Prefetch('episode_info_model', queryset=self.animate_episode_info_model.objects.filter(done=True))
        queryset = self.animate_info_model.objects.prefetch_related(prefetch).filter(
            episode_info_model__done=True).distinct()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
