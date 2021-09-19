from django.urls import path
from Api.views import WeekAnimateView, TestView, MyselfAnimateInfoView

app_name = 'api'

myself_url = [
    path('myself/week-animate/', WeekAnimateView.as_view(), name='myself_week_animate'),
    path('myself/animate-info/', MyselfAnimateInfoView.as_view(), name='myself_animate_info'),
]

test_url = [
    path('test/', TestView.as_view(), name='test'),
]

urlpatterns = myself_url + test_url
