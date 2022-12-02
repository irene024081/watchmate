from django.urls import path, include
from watchlist_app.api.views import ReviewDetail,ReviewList,WatchListAV, WatchListDetailAV, StreamPlatformAV, StreamPlatformDetailsAV

urlpatterns = [
    path('list/', WatchListAV.as_view(), name = 'watch_list'),
    path('<int:pk>', WatchListDetailAV.as_view(), name = 'movie_details'),
    path('stream/', StreamPlatformAV.as_view(), name = 'stream'),
    path('stream/<int:pk>', StreamPlatformDetailsAV.as_view(), name = 'stream_details'),
    path('review', ReviewList.as_view(), name = 'review_list'),
    path('review/<int:pk>', ReviewDetail.as_view(), name='review_details'),
]