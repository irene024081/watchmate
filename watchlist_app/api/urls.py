from django.urls import path, include
from watchlist_app.api.views import WatchListAV, WatchListDetailAV, StreamPlatformAV, StreamPlatformDetailsAV

urlpatterns = [
    path('list/', WatchListAV.as_view(), name = 'watch_list'),
    path('<int:pk>', WatchListDetailAV.as_view(), name = 'movie_details'),
    path('stream/', StreamPlatformAV.as_view(), name = 'stream'),
    path('stream/<int:pk>', StreamPlatformDetailsAV.as_view(), name = 'stream_details'),
]