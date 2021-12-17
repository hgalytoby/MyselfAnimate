from django.urls import path
from Api.views import myself, TestView, my, anime1

from project.settings import DEBUG

app_name = 'api'

myself_api = [
    path('myself/week-animate/', myself.WeekAnimateView.as_view(), name='myself_week_animate'),
    path('myself/animate-info/', myself.AnimateInfoView.as_view(), name='myself_animate_info'),
    path('myself/animate-info/<str:animate_id>/episode-info/', myself.AnimateInfoEpisodeView.as_view(),
         name='myself_animate_info_episode_info'),
    path('myself/finish-list/', myself.FinishListView.as_view(), name='myself_finish_list'),
    path('myself/finish-animate/', myself.FinishAnimateView.as_view(), name='myself_finish_animate'),
    path('myself/animate-episode-info/<str:pk>/', myself.AnimateEpisodeInfoView.as_view(), name='myself_animate_episode_info'),
    path('myself/download/<str:pk>/', myself.DownloadView.as_view(), name='myself_download'),
    path('myself/animate-episode-done/', myself.AnimateEpisodeDoneView.as_view(), name='myself_animate_episode_done'),
]

my_api = [
    path('my/log/system/', my.SystemView.as_view(), name='my_log_system'),
    path('my/log/history/', my.HistoryView.as_view(), name='my_log_history'),
    path('my/log/', my.LogView.as_view(), name='my_log'),
]

anime1_api = [
    path('anime1/home-animate/', anime1.HomeAnimateView.as_view(), name='anime1_home_animate'),
    path('anime1/animate-info/', anime1.AnimateInfoView.as_view(), name='anime1_animate_info'),
]

test_api = [
    path('test/', TestView.as_view(), name='test'),
]

urlpatterns = myself_api + my_api + anime1_api

if DEBUG:
    urlpatterns += test_api
