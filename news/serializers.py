from rest_framework import serializers
from .models import News
from admin_actions.models import Admin

class NewsSerializer(serializers.ModelSerializer):
    admin_name = serializers.CharField(source='admin_id.username', read_only=True)  
    
    class Meta:
        model = News
        fields = '__all__'
        read_only_fields = ('news_id', 'created_at', 'updated_at')
    
    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()
    
    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value.strip()


class NewsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['title', 'content', 'image', 'admin_id', 'is_published']
    
    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()
    
    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value.strip()