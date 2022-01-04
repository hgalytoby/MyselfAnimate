from django.urls import path

from Api.views import MyselfWeekAnimateView, MyselfAnimateInfoView, MyselfAnimateInfoEpisodeView, MyselfFinishListView, \
    MyselfFinishAnimateView, MyselfAnimateEpisodeInfoView, MyselfDownloadView, MyselfAnimateEpisodeDoneView, \
    MySystemView, MyHistoryView, MyLogView, Anime1AnimateListView, Anime1AnimateInfoView, TestView, \
    Anime1AnimateInfoEpisodeView, Anime1AnimateEpisodeDoneView
from project.settings import DEBUG

app_name = 'api'

myself_api = [
    path('myself/week-animate/', MyselfWeekAnimateView.as_view(), name='myself_week_animate'),
    path('myself/animate-info/', MyselfAnimateInfoView.as_view(), name='myself_animate_info'),
    path('myself/animate-info/<str:animate_id>/episode-info/', MyselfAnimateInfoEpisodeView.as_view(),
         name='myself_animate_info_episode_info'),
    path('myself/finish-list/', MyselfFinishListView.as_view(), name='myself_finish_list'),
    path('myself/finish-animate/', MyselfFinishAnimateView.as_view(), name='myself_finish_animate'),
    path('myself/animate-episode-info/<str:pk>/', MyselfAnimateEpisodeInfoView.as_view(),
         name='myself_animate_episode_info'),
    path('myself/download/<str:pk>/', MyselfDownloadView.as_view(), name='myself_download'),
    path('myself/animate-episode-done/', MyselfAnimateEpisodeDoneView.as_view(), name='myself_animate_episode_done'),
]

my_api = [
    path('my/log/system/', MySystemView.as_view(), name='my_log_system'),
    path('my/log/history/', MyHistoryView.as_view(), name='my_log_history'),
    path('my/log/', MyLogView.as_view(), name='my_log'),
]

anime1_api = [
    path('anime1/animate-list/', Anime1AnimateListView.as_view(), name='anime1_animate_list'),
    path('anime1/animate-info/', Anime1AnimateInfoView.as_view(), name='anime1_animate_info'),
    path('anime1/animate-info/<str:animate_id>/episode-info/', Anime1AnimateInfoEpisodeView.as_view(),
         name='anime1_animate_info_episode_info'),
    path('anime1/animate-episode-done/', Anime1AnimateEpisodeDoneView.as_view(), name='anime1_animate_episode_done'),
]

test_api = [
    path('test/', TestView.as_view(), name='test'),
]

urlpatterns = myself_api + my_api + anime1_api

if DEBUG:
    urlpatterns += test_api
