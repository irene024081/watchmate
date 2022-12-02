from django.urls import path, include
from watchlist_app.api.views import (ReviewDetail,ReviewList,
                                    WatchListAV, WatchListDetailAV, 
                                    #StreamPlatformAV, StreamPlatformDetailsAV,
                                    StreamPlatformVS)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('stream', StreamPlatformVS, basename='stream_platform')
urlpatterns = [
    path('list/', WatchListAV.as_view(), name = 'watch_list'),
    path('<int:pk>', WatchListDetailAV.as_view(), name = 'movie_details'),
    path('',include(router.urls)),
    # path('stream/', StreamPlatformAV.as_view(), name = 'stream'),
    # path('stream/<int:pk>', StreamPlatformDetailsAV.as_view(), name = 'stream_details'),
    # path('stream/<int:pk>/review', ReviewList.as_view(), name = 'review_list'),
    # path('stream/review/<int:pk>', ReviewDetail.as_view(), name='review_details'),
]