from Tools.db import DB


class BaseAnimateEpisodeDone:
    def list(self, request, *args, **kwargs):
        queryset = DB.Anime1.filter_episode_done()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)