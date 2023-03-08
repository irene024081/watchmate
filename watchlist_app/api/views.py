from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, mixins, generics, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.throttling import ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend



from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly

from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import (WatchListSerializer, 
                                           StreamPlatformSerializer, ReviewSerializer)
from watchlist_app.api.throtlling import ReviewListThrottle


class UserReview(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # throttle_classes = [ReviewListThrottle]


    def get_queryset(self):
        username = self.kwargs['username']
        return Review.objects.filter(review_user__username=username)

class ReviewList(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [ReviewListThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']


    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk = pk)
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=movie, review_user=review_user)
        if review_queryset.exists():
            raise ValidationError("you have already reviewed!")
        
        if movie.num_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = (movie.avg_rating * movie.num_rating + 
                                serializer.validated_data['rating'])/(movie.num_rating + 1)
        movie.num_rating += 1
        movie.save()
        
        serializer.save(watchlist=movie, review_user = review_user)
    
        
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review_detail'
    
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk = pk)
 
        serializer.save(watchlist=movie)
        
# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
        
class WatchListAV(APIView):
    permission_class = [IsAdminOrReadOnly]
    
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class WatchListDetailAV(APIView):
    permission_class = [IsAdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error':'Not Exist'}, status = status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
    
    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

# model viewsets
class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_class = [IsAdminOrReadOnly]
    

# # viewsets
# class StreamPlatformVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many = True)
#         return Response(serializer.data)
    
#     def retrieve(self, request, pk = None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
    
    
class StreamPlatformAV(APIView):
    permission_class = [IsAdminOrReadOnly]
    
    def get(self, request):
        platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platforms, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class StreamPlatformDetailsAV(APIView):
    permission_class = [IsAdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk = pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error':
            'Not Exist'}, status = status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)
    
    def put(self, request, pk):
        platform = StreamPlatform.objects.get(pk = pk)
        serializer = StreamPlatformSerializer(platform, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def delete(self, request, pk):
        platform = StreamPlatform.objects.get(pk = pk)    
        platform.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
