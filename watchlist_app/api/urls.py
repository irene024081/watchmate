from django.urls import path, include
from watchlist_app.api.views import (ReviewDetail,ReviewList,
                                    WatchListAV, WatchListDetailAV, 
                                    #StreamPlatformAV, StreamPlatformDetailsAV,
                                    StreamPlatformVS,
                                    UserReview)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'stream', StreamPlatformVS, basename='stream_platform')
urlpatterns = [
    path('list/', WatchListAV.as_view(), name = 'watch_list'),
    path('<int:pk>/', WatchListDetailAV.as_view(), name = 'movie_details'),
    path('',include(router.urls)),
    # path('stream/', StreamPlatformAV.as_view(), name = 'stream'),
    # path('stream/<int:pk>', StreamPlatformDetailsAV.as_view(), name = 'stream_details'),
    path('<int:pk>/reviews/', ReviewList.as_view(), name = 'review_list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review_details'),
    path('reviews/<str:username>/', UserReview.as_view(), name='user_review_details'),
]