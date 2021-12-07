from django.urls import path
from Api.views import WeekAnimateView, TestView, AnimateInfoView, FinishListView, FinishAnimateView, SystemView, \
    HistoryView, AnimateEpisodeInfoView, DownloadView, AnimateEpisodeDoneView, AnimateInfoEpisodeView, LogView
from project.settings import DEBUG

app_name = 'api'

myself_api = [
    path('myself/week-animate/', WeekAnimateView.as_view(), name='myself_week_animate'),
    path('myself/animate-info/', AnimateInfoView.as_view(), name='myself_animate_info'),
    path('myself/animate-info/<str:animate_id>/episode-info/', AnimateInfoEpisodeView.as_view(),
         name='myself_animate_info_episode_info'),
    path('myself/finish-list/', FinishListView.as_view(), name='myself_finish_list'),
    path('myself/finish-animate/', FinishAnimateView.as_view(), name='myself_finish_animate'),
    path('myself/animate-episode-info/<str:pk>/', AnimateEpisodeInfoView.as_view(), name='myself_animate_episode_info'),
    path('myself/download/<str:pk>/', DownloadView.as_view(), name='myself_download'),
    path('myself/animate-episode-done/', AnimateEpisodeDoneView.as_view(), name='myself_animate_episode_done'),
]

my_api = [
    path('my/log/system/', SystemView.as_view(), name='my_log_system'),
    path('my/log/history/', HistoryView.as_view(), name='my_log_history'),
    path('my/log/', LogView.as_view(), name='my_log'),
]

test_api = [
    path('test/', TestView.as_view(), name='test'),
]

urlpatterns = myself_api + my_api

if DEBUG:
    urlpatterns += test_api
