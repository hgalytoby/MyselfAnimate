from django.urls import path

from Api.views import MyselfWeekAnimateView, MyselfAnimateInfoView, MyselfAnimateInfoEpisodeView, MyselfFinishListView, \
    MyselfFinishAnimateView, MyselfAnimateEpisodeDoneView, \
    MySystemView, MyHistoryView, MyLogView, Anime1AnimateListView, Anime1AnimateInfoView, TestView, \
    Anime1AnimateInfoEpisodeView, Anime1AnimateEpisodeDoneView, MyselfUrlAnimate, MySettingsView, Anime1MenuSeasonView, \
    Anime1SeasonView, MyselfDestroyManyAnimate, Anime1DestroyManyAnimateView
from project.settings import DEBUG

app_name = 'api'

myself_api = [
    path('myself/week-animate/', MyselfWeekAnimateView.as_view({
        'get': 'list'
    })),
    path('myself/animate-info/', MyselfAnimateInfoView.as_view({
        'get': 'list'
    })),
    path('myself/animate-info/<str:animate_id>/episode-info/', MyselfAnimateInfoEpisodeView.as_view({
        'get': 'list'
    })),
    path('myself/finish-list/', MyselfFinishListView.as_view({
        'get': 'list'
    })),
    path('myself/finish-animate/', MyselfFinishAnimateView.as_view({
        'get': 'list'
    })),
    path('myself/animate-episode-done/', MyselfAnimateEpisodeDoneView.as_view({
        'get': 'list',
    })),
    path('myself/url-search/', MyselfUrlAnimate.as_view({
        'get': 'list'
    })),
    path('myself/destroy-many-animate/', MyselfDestroyManyAnimate.as_view({
        'delete': 'destroy',
    })),

]

my_api = [
    path('my/log/system/', MySystemView.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('my/log/history/', MyHistoryView.as_view({
        'get': 'list',
    })),
    path('my/log/', MyLogView.as_view({
        'get': 'list',
    })),
    path('my/settings/', MySettingsView.as_view({
        'get': 'list',
        'put': 'update',
    })),
]

anime1_api = [
    path('anime1/animate-list/', Anime1AnimateListView.as_view({
        'get': 'list',
    })),
    path('anime1/animate-info/', Anime1AnimateInfoView.as_view({
        'post': 'create',
    })),
    path('anime1/animate-info/<str:animate_id>/episode-info/', Anime1AnimateInfoEpisodeView.as_view({
        'get': 'list',
    })),
    path('anime1/animate-episode-done/', Anime1AnimateEpisodeDoneView.as_view({
        'get': 'list',
    })),
    path('anime1/home-menu/', Anime1MenuSeasonView.as_view({
        'get': 'list',
    })),
    path('anime1/season/<str:season>/', Anime1SeasonView.as_view({
        'get': 'list',
    })),
    path('anime1/destroy-many-animate/', Anime1DestroyManyAnimateView.as_view({
        'delete': 'destroy',
    })),
]

test_api = [
    path('test/', TestView.as_view()),
]

urlpatterns = myself_api + my_api + anime1_api

if DEBUG:
    urlpatterns += test_api
