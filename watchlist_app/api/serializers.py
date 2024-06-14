from rest_framework import serializers
from watchlist_app.models import WatchList,StreamPlatform,Review

# class MovieSerializer(serializers.Serializer):
# 	id = serializers.IntegerField(read_only=True)
# 	name = serializers.CharField()
# 	description = serializers.CharField()
# 	active = serializers.BooleanField()

# 	def create(self,validated_data):
# 		return Movie.objects.create(**validated_data)

# 	def update(self,instance,validated_data):
# 		instance.name = validated_data.get('name',instance.name)
# 		instance.description = validated_data.get('description',instance.description)
# 		instance.active = validated_data.get('active',instance.active)
# 		instance.save()
# 		return instance

# 	def validate_name(self,value):
# 		if len(value) < 2:
# 			raise serializers.ValidationError("Name is too short");
# 		return value
	
# 	def validate(self,data):
# 		if data['name'] == data['description']:
# 			raise serializers.ValidationError("Title and Description should be dt")
# 		else:
# 			return data



class ReviewSerializer(serializers.ModelSerializer):
	review_user = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = Review
		exclude = ('watchlist',)



class WatchListSerializer(serializers.ModelSerializer):
	reviews = ReviewSerializer(many=True,read_only=True)
	class Meta:
		model = WatchList
		fields = '__all__'


class StreamPlatformSerializer(serializers.ModelSerializer):
	# watchlist = WatchListSerializer(many=True,read_only=True)
	# watchlist = serializers.StringRelatedField(many=True)
    #watchlist = serializers.HyperlinkedRelatedField(
    	# many=True,
    	# read_only=True,
    	# view_name='movie-detail')
    watchlist = WatchListSerializer(many=True,read_only=True)
    class Meta:
    	model = StreamPlatform
    	fields = "__all__"






	# class Meta:
	# 	model = StreamPlatform
	# 	fields = "__all__"

		# def validate(self,data):
		# 	if data['name'] == data['description']:
		# 		raise serializers.ValidationError("Title and description should be different!")
		# 	else:
		# 		return data

		# def validate_name(self,value):
		# 	if len(value) < 2:
		# 		raise serializers.ValidationError("Name is too short")
		# 	else:
		# 		return value


