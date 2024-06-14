from watchlist_app.models import WatchList,StreamPlatform,Review
from watchlist_app.api.serializers import (WatchListSerializer,StreamPlatformSerializer,ReviewSerializer)
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from watchlist_app.api.permissions import AdminOrReadOnly,ReviewUserOrReadOnly
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle

class ReviewCreate(generics.CreateAPIView):
	serializer_class = ReviewSerializer
	permission_classes = [IsAuthenticated]
	throttle_classes = [ReviewCreateThrottle]

	def get_queryset(self):
		return Review.objects.all()

	def perform_create(self,serializer):
		pk = self.kwargs.get('pk')
		watchlist = WatchList.objects.get(pk=pk)

		review_user = self.request.user
		review_queryset = Review.objects.filter(watchlist=watchlist,review_user=review_user)

		if review_queryset.exists():
			raise ValidationError("You have already reviewed this movie!")

		if watchlist.number_rating == 0:
			watchlist.avg_rating = serializer.validated_data['rating']
		else:
			watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2
		watchlist.number_rating = watchlist.number_rating + 1
		watchlist.save()
		
		serializer.save(watchlist=watchlist,review_user=review_user)

# @api_view(['GET','POST'])
# def movie_list(request):
# 	if request.method == 'GET':
# 		movies = Movie.objects.all()
# 		serializer = MovieSerializer(movies,many=True)
# 		return Response(serializer.data)

# 	if request.method == 'POST':
# 		serializer = MovieSerializer(data=request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data)
# 		else:
# 			return Response(serializer.errors)
# @api_view(['GET','PUT','DELETE'])
# def movie_detail(request,pk):
# 	if request.method == "GET":
# 		try:
# 			movie = Movie.objects.get(pk=pk)
# 		except Movie.DoesNotExist:
# 			return Response({'Error':'Movie not found'},status=status.HTTP_400_BAD_REQUEST)
# 		serializer = MovieSerializer(movie)
# 		return Response(serializer.data)
# 	if request.method == 'PUT':
# 		movie = Movie.objects.get(pk=pk)
# 		serializer = MovieSerializer(movie, data=request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data)
# 		else:
# 			return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
# 	if request.method == 'DELETE':
# 		movie = Movie.objects.get(pk=pk)
# 		movie.delete()
# 		return Response(status=status.HTTP_204_NO_CONTENT)

# class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
# 	queryset = Review.objects.all()
# 	serializer_class = ReviewSerializer

# 	def get(self,request,*args,**kwargs):
# 		return self.retrieve(request,*args,**kwargs)


# class ReviewList(mixins.ListModelMixin,
# 	             mixins.CreateModelMixin,
# 	             generics.GenericAPIView):
# 	queryset = Review.objects.all()
# 	serializer_class = ReviewSerializer

# 	def get(self,request,*args,**kwargs):
# 		return self.list(request,*args,**kwargs)

# 	def post(self,request,*args,**kwargs):
# 		return self.create(request,*args,**kwargs)

# class StreamPlatform(ViewSets.ViewSet):

# 	def list(self,request):
# 		queryset = StreamPlatform.objects.all()
# 		serializer = StreamPlatformSerializer(queryset,many=True)
# 		return Response(serializer.data)

# 	def retrieve(self,request,pk=None):
# 		queryset = StreamPlatform.objects.all()
# 		watchlist = get_object_or_404(queryset,pk=pk)
# 		serializer = StreamPlatformSerializer(watchlist)
# 		return Response(serializer.data)


class StreamPlatformAV(APIView):
	def get(self,request):
		platform = StreamPlatform.objects.all()
		serializer = StreamPlatformSerializer(platform,many=True,context={'request':request})
		return Response(serializer.data)

	def post(self,request):
		serializer = StreamPlatformSerializer(data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors)

class StreamPlatformVS(viewsets.ModelViewSet):
	# def list(self,request):
	# 	queryset = StreamPlatform.objects.all()
	# 	serreializer = StreamPlatformSerializer(queryset,many=True)
	# 	return Response(serializer.data)

	# def retrieve(self,request,pk=None):
	# 	queryset = StreamPlatform.objects.all()
	# 	watchlist = get_object_or_404(queryset,pk=pk)
	# 	serializer = StreamPlatformSerializer(StreamPlatform)
	# 	return Response(serializer.data)

	# def create(self,request):
	# 	serializer = StreamPlatformSerializer(data=request.data)
	# 	if serializer.is_valid():
	# 		serializer.save()
	# 		return Response(serializer.data)
	# 	else:
	# 		return Response(serializer.errors)
	queryset = StreamPlatform.objects.all()
	serializer_class = StreamPlatformSerializer
	permission_classes = [AdminOrReadOnly]


class StreamPlatformDetailAV(APIView):
	permission_classes = [AdminOrReadOnly]

	def get(self,request,pk):
		try:
			platform = StreamPlatform.objects.get(pk=pk)
		except StreamPlatform.DoesNotExist:
			return Response({'error': 'Not Found'},
				status=status.HTTP_404_NOT_FOUND)
		serializer = StreamPlatformSerializer(platform,context={'request':request})
		return Response(serializer.data)

	def put(self,request,pk):
		platform = StreamPlatform.objects.get(pk=pk)
		serializer = StreamPlatformSerializer(platform,data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

	def delete(self,request,pk):
		platform = StreamPlatform.objects.get(pk=pk)
		platform.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)



class WatchListAV(APIView):
	permission_classes = [AdminOrReadOnly]

	def get(self,request):
		movies = WatchList.objects.all()
		serializer = WatchListSerializer(movies,many=True)
		return Response(serializer.data)

	def post(self,request):
		serializer = WatchListSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors)

class WatchDetailAV(APIView):
	permission_classes = [AdminOrReadOnly]
	def get(self,request,pk):
		try:
			movie = WatchList.objects.get(pk=pk)
		except Movie.DoesNotExist:
			return Response({'Error':'Movie not found'},status=status.HTTP_400_BAD_REQUEST)
		serializer = MovieSerializer(movie)
		return Response(serializer.data) 

	def put(self,request,pk):
		movie = WatchList.objects.get(pk=pk)
		serializer = MovieSerializer(movie, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

	def delete(self,request,pk):
		movie = WatchList.objects.get(pk=pk)
		movie.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

# class ReviewList(generics.ListAPIView):
# 	# queryset = Review.objects.all()
# 	serializer_class = ReviewSerializer

# 	def get_queryset(self):
# 		pk = self.kwargs['pk']
# 		return Review.objects.filter(watchlist=pk)

# class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
# 	queryset = Review.objects.all()
# 	serializer_class = ReviewSerializer
# class ReviewCreate(generics.CreateAPIView):
# 	serializer_class = ReviewSerializer
# 	def perform_create(self,serializer):
# 		pk = self.kwargs.get('pk')
# 		watchlist = WatchList.objects.get(pk=pk)
# 		serializer.save(watchlist=watchlist)


class ReviewList(generics.ListAPIView):
	
	serializer_class = ReviewSerializer
	#permission_classes = [IsAuthenticated]
	throttle_classes = [ReviewvListThrottle,AnonRateThrottle]

	def get_queryset(self):
		pk = self.kwargs['pk']
		return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Review.objects.all()
	serializer_class = ReviewSerializer
	permission_classes = [ReviewUserOrReadOnly]
























