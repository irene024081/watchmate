from rest_framework import serializers
from watchlist_app.models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"
        # other ways to define fields, select some of the fields
        # or exclude some of the fields
        
        #fields = ['id', 'name', 'description']
        #exclude = ['name']
    
    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name is too short")
        else:
            return value

    def validate(self, data):
        if data.get('name') == data['description']:
            raise serializers.ValidationError("Title and description cannot be same")
        return data
        
    
    
## can use plan serializer using the following code to replace
## the above ModelSerializer definition

# def name_length(name):
#     if len(name) < 2:
#         raise serializers.ValidationError("Name is too short")
    
# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()
    
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
      
#     # field level validation    
#     # def validate_name(self, value):
        
#     #     if len(value) < 2:
#     #         raise serializers.ValidationError("Name is too short")
#     #     else:
#     #         return value
    
#     def validate(self, data):
#         if data.get('name') == data['description']:
#             raise serializers.ValidationError("Title and description cannot be same")
#         return data
        
    