from rest_framework import serializers
from .models import Blog, Comments

class BlogSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = '__all__'
        
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields ='__all__'
        