from django.urls import path
from Api.views import WeekAnimateView, TestView

app_name = 'api'

myself_url = [
    path('week-animate/', WeekAnimateView.as_view(), name='myself'),
]

test_url = [
    path('test/', TestView.as_view(), name='test'),
]

urlpatterns = myself_url + test_url
