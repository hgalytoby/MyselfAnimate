from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView

from Api.serializers import FinishAnimateSerializer, AnimateEpisodeInfoSerializer
from Database.models import FinishAnimateModel, AnimateEpisodeInfoModel, AnimateEpisodeTsModel
from Tools.db import DB
from Tools.myself import Myself
from Tools.tools import req_bytes
from project.settings import MEDIA_PATH


class WeekAnimateView(APIView):
    def get(self, request):
        data = Myself.week_animate()
        # print(data)
        # data = {'Monday': [{'name': '星期一的豐滿 第二季', 'url': 'thread-47902-1-1.html', 'update_color': 'color: #0000FF;',
        #                      'update': '(更新：第 05 集)'},
        #                     {'name': '加油！同期醬', 'url': 'thread-47903-1-1.html', 'update_color': 'color: #0000FF;',
        #                      'update': '(更新：第 05 集)'},
        #                     {'name': '月與萊卡與吸血公主', 'url': 'thread-47938-1-1.html', 'update_color': 'color: #0000FF;',
        #                      'update': '(更新：第 03 集)'}, {'name': '王者天下 KINGDOM 第三季', 'url': 'thread-45395-1-1.html',
        #                                                 'update_color': 'color: #0000FF;', 'update': '(更新：第 26 集)'},
        #                     {'name': '鬼滅之刃 無限列車篇', 'url': 'thread-47966-1-1.html', 'update_color': 'color: #0000FF;',
        #                      'update': '(更新：第 02 集)'},
        #                     {'name': '無職轉生', 'url': 'thread-46571-1-1.html', 'update_color': 'color: #0000FF;',
        #                      'update': '(更新：第 14 集)'},
        #                     {'name': 'Love Live! Superstar!!', 'url': 'thread-47767-1-1.html',
        #                      'update_color': 'color: #0000FF;', 'update': '(更新：第 11 集)'}], 'Tuesday': [
        #     {'name': '逆轉世界的電池少女', 'url': 'thread-47969-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 02 集)'},
        #     {'name': '鋼彈創壞者 對戰風雲錄', 'url': 'thread-47991-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 01 集)'},
        #     {'name': '進化果實', 'url': 'thread-47945-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 03 集)'},
        #     {'name': 'Assault Lily Fruits', 'url': 'thread-47802-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 05 集)'}], 'Wednesday': [
        #     {'name': '平家物語', 'url': 'thread-47908-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 05 集)'},
        #     {'name': '暗殺貴族', 'url': 'thread-47948-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 03 集)'},
        #     {'name': '鍵等', 'url': 'thread-47974-1-1.html', 'update_color': 'color: #0000FF;', 'update': '(更新：第 02 集)'},
        #     {'name': '宿命迴響：命運節拍', 'url': 'thread-47947-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 03 集)'}], 'Thursday': [
        #     {'name': '通靈王 重製版', 'url': 'thread-47279-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 27 集)'},
        #     {'name': '緋紅結繫', 'url': 'thread-47650-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 17 集)'},
        #     {'name': '真正的夥伴', 'url': 'thread-47951-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 03 集)'},
        #     {'name': 'Muv-Luv Alternative', 'url': 'thread-47949-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 03 集)'},
        #     {'name': '古見同學有交流障礙症', 'url': 'thread-47950-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 03 集)'},
        #     {'name': '桃子男孩渡海而來', 'url': 'thread-47670-1-1.html', 'update_color': 'color: #FF00FF;',
        #      'update': '(更新：全 12 集)'}], 'Friday': [
        #     {'name': '寵物小精靈', 'url': 'thread-45306-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 84 集)'},
        #     {'name': 'SAKUGAN', 'url': 'thread-47953-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 03 集)'},
        #     {'name': '白沙的Aquatope', 'url': 'thread-47746-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 16 集)'},
        #     {'name': '白金終局', 'url': 'thread-47985-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 02 集)'},
        #     {'name': 'SELECTION PROJECT', 'url': 'thread-47932-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 03 集)'}], 'Saturday': [
        #     {'name': '半妖的夜叉姬 第二季', 'url': 'thread-47931-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 04 集)'},
        #     {'name': '藍色時期', 'url': 'thread-47913-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 05 集)'},
        #     {'name': '勇者鬥惡龍 達伊的大冒險', 'url': 'thread-46160-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 54 集)'},
        #     {'name': '結城友奈是勇者 第三季', 'url': 'thread-47923-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 04 集)'},
        #     {'name': '大正處女御伽話', 'url': 'thread-47957-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 03 集)'},
        #     {'name': '異世界食堂 第二季', 'url': 'thread-47929-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 04 集)'},
        #     {'name': '讓你的耳朵感到幸福', 'url': 'thread-47982-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 01 集)'},
        #     {'name': '世界盡頭的聖騎士', 'url': 'thread-47961-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 02 集)'}], 'Sunday': [
        #     {'name': '三角窗外是黑夜', 'url': 'thread-47954-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 03 集)'},
        #     {'name': '甜夢貓 Mix', 'url': 'thread-47293-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 27 集)'},
        #     {'name': '賈希大人不氣餒', 'url': 'thread-47822-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 11 集)'},
        #     {'name': '海賊王女', 'url': 'thread-47849-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 11 集)'},
        #     {'name': '陰陽眼見子', 'url': 'thread-47936-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 03 集)'},
        #     {'name': '博人傳 -火影新世代-', 'url': 'thread-42259-1-1.html', 'update_color': 'color: #FF0000;',
        #      'update': '(更新：第 220 集)'},
        #     {'name': 'Tropical-Rouge！', 'url': 'thread-47124-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 33 集)'},
        #     {'name': '境界觸發者 第三季', 'url': 'thread-47976-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 02 集)'},
        #     {'name': 'Build Divide', 'url': 'thread-47979-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 02 集)'},
        #     {'name': '魯邦三世 PART6', 'url': 'thread-47964-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 01 集)'},
        #     {'name': '前輩有夠煩', 'url': 'thread-47962-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 02 集)'},
        #     {'name': '86－不存在的戰區', 'url': 'thread-47281-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 14 集)'},
        #     {'name': '海賊王', 'url': 'thread-42657-1-1.html', 'update_color': 'color: #FF0000;',
        #      'update': '(更新：第 995 集)'},
        #     {'name': '數碼寶貝 幽靈遊戲', 'url': 'thread-47934-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 02 集)'},
        #     {'name': '死神少爺與黑女僕', 'url': 'thread-47704-1-1.html', 'update_color': 'color: #FF00FF;',
        #      'update': '(更新：全 12 集)'},
        #     {'name': '歌劇少女', 'url': 'thread-47750-1-1.html', 'update_color': 'color: #0000FF;',
        #      'update': '(更新：第 10 集)'}]}
        if data:
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class AnimateInfoView(APIView):
    def get(self, request):
        url = request.query_params.get('url')
        animate_url = f'https://myself-bbs.com/{url}'
        data = Myself.animate_info(url=animate_url)
        image = req_bytes(url=data['image'])
        model = DB.Myself.update_or_create_animate_info_model(data=data, image=image)
        models = DB.Myself.create_many_animate_episode_models(data, owner=model)
        data['image'] = f'{MEDIA_PATH}{model.image.url}'
        data['id'] = model.id
        data['video'] = [m.to_dict() for m in models]
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


class AnimateEpisodeInfoView(RetrieveUpdateAPIView):
    serializer_class = AnimateEpisodeInfoSerializer
    queryset = AnimateEpisodeInfoModel.objects.select_related('owner').all()

    def put(self, request, *args, **kwargs):
        if request.data.get('download'):
            model = AnimateEpisodeInfoModel.objects.get(pk=kwargs.get('pk'))
            AnimateEpisodeTsModel.objects.filter(owner=model).delete()
        return self.update(request, *args, **kwargs)
