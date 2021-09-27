from django.urls import path
from Api.views import WeekAnimateView, TestView, AnimateInfoView, FinishListView, FinishAnimateView, LogView, \
    HistoryView

app_name = 'api'

myself_url = [
    path('myself/week-animate/', WeekAnimateView.as_view(), name='myself_week_animate'),
    path('myself/animate-info/', AnimateInfoView.as_view(), name='myself_animate_info'),
    path('myself/finish-list/', FinishListView.as_view(), name='myself_finish_list'),
    path('myself/finish-animate/', FinishAnimateView.as_view(), name='myself_finish_animate'),
]

my_url = [
    path('my/log/', LogView.as_view(), name='my_log'),
    path('my/history/', HistoryView.as_view(), name='my_history'),
]

test_url = [
    path('test/', TestView.as_view(), name='test'),
]

urlpatterns = myself_url + test_url + my_url
