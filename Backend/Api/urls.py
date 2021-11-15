from django.urls import path
from Api.views import WeekAnimateView, TestView, AnimateInfoView, FinishListView, FinishAnimateView, LogView, \
    HistoryView, AnimateEpisodeInfoView, DownloadView, AnimateEpisodeDoneView

app_name = 'api'

myself_api = [
    path('myself/week-animate/', WeekAnimateView.as_view(), name='myself_week_animate'),
    path('myself/animate-info/', AnimateInfoView.as_view(), name='myself_animate_info'),
    path('myself/finish-list/', FinishListView.as_view(), name='myself_finish_list'),
    path('myself/finish-animate/', FinishAnimateView.as_view(), name='myself_finish_animate'),
    path('myself/animate-episode-info/<str:pk>/', AnimateEpisodeInfoView.as_view(), name='myself_animate_episode_info'),
    path('myself/download/<str:pk>/', DownloadView.as_view(), name='myself_download'),
    path('myself/animate-episode-done/', AnimateEpisodeDoneView.as_view(), name='myself_animate_episode_done'),
]

my_api = [
    path('my/log/', LogView.as_view(), name='my_log'),
    path('my/history/', HistoryView.as_view(), name='my_history'),
]

test_api = [
    path('test/', TestView.as_view(), name='test'),
]

urlpatterns = myself_api + my_api + test_api
