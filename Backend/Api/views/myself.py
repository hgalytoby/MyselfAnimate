from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from Api.serializers import FinishAnimateSerializer
from Database.models import FinishAnimateModel, AnimateEpisodeInfoModel
from Tools.db import DB
from Tools.myself import Myself
from Tools.tools import req_bytes
from project.settings import MEDIA_ROOT, MEDIA_PATH


class WeekAnimateView(APIView):
    def get(self, request):
        data = Myself.week_animate()
        if data:
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class AnimateInfoView(APIView):
    def get(self, request):
        # url = request.query_params.get('url')
        # animate_url = f'https://myself-bbs.com/{url}'
        # data = Myself.animate_info(url=animate_url)
        # image = req_bytes(url=data['image'])
        # model = DB.Myself.update_or_create_animate_info(data=data, image=image)
        # models = DB.Myself.many_create_animate_episode(data, parent_model=model)
        # data['image'] = f'{MEDIA_PATH}{model.image.url}'
        # data['id'] = model.id
        # data['video'] = [m.to_dict() for m in models]
        # print(data)
        data = {'animate_type': '校園 / 勵志', 'premiere_date': '2021年07月11日', 'episode': '未定', 'author': '矢立肇',
                'official_website': 'https://www.lovelive-anime.jp/yuigaoka/', 'remarks': '',
                'synopsis': '結丘女子高等學校，首位入學生來到了這所位於表參道、原宿和青山這三條街區之間的新學校。沒有歷史、沒有前輩、名字也完全不為人所知，在這間盡是「沒有」的學校，以澀谷香音為中心的五名少女和“學園偶像”遇上了。\n\r\n我果然很喜歡歌唱！ 想透過歌唱……實現點什麼！！渺小的星星們，她們宏大的想法重合著——。白紙一張，擁有著無限可能性的她們的「大家一起實現的故事（School idol project）」。飛翔吧！我們的LoveLive！',
                'image': '/static/uploads/Myself/Love%20Live!%20Superstar!!/big_Love_Live_Superstar.webp',
                'url': 'https://myself-bbs.com/thread-47767-1-1.html', 'name': 'Love Live! Superstar!!',
                'video': [
                    {'id': 1, 'name': '第 01 話', 'url': 'https://v.myself-bbs.com/vpx/47767/001', 'download': False,
                     'done': False, 'owner_id': 6},
                    {'id': 2, 'name': '第 02 話', 'url': 'https://v.myself-bbs.com/vpx/47767/002', 'download': False,
                     'done': False, 'owner_id': 6},
                    {'id': 3, 'name': '第 03 話', 'url': 'https://v.myself-bbs.com/vpx/47767/003', 'download': False,
                     'done': False, 'owner_id': 6},
                    {'id': 4, 'name': '第 04 話', 'url': 'https://v.myself-bbs.com/vpx/47767/004', 'download': False,
                     'done': False, 'owner_id': 6},
                    {'id': 5, 'name': '第 05 話', 'url': 'https://v.myself-bbs.com/vpx/47767/005', 'download': False,
                     'done': False, 'owner_id': 6},
                    {'id': 6, 'name': '第 06 話', 'url': 'https://v.myself-bbs.com/vpx/47767/006', 'download': False,
                     'done': False, 'owner_id': 6},
                    {'id': 7, 'name': '第 07 話', 'url': 'https://v.myself-bbs.com/vpx/47767/007', 'download': False,
                     'done': False, 'owner_id': 6},
                    {'id': 8, 'name': '第 08 話', 'url': 'https://v.myself-bbs.com/vpx/47767/008', 'download': False,
                     'done': False, 'owner_id': 6},
                    {'id': 9, 'name': '第 09 話', 'url': 'https://v.myself-bbs.com/vpx/47767/009', 'download': False,
                     'done': False, 'owner_id': 6}], 'id': 1}

        if data:
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class FinishListView(APIView):
    def get(self, request):
        data = Myself.finish_list()
        if data:
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class FinishAnimateView(ListAPIView):
    serializer_class = FinishAnimateSerializer
    queryset = FinishAnimateModel.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

