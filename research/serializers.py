from rest_framework import serializers
from .models import Research_articles
from admin_actions.models import Admin

class ResearchArticleSerializer(serializers.ModelSerializer):
    admin_name = serializers.CharField(source='admin_id.username', read_only=True)

    class Meta:
        model = Research_articles
        fields = '__all__'
        read_only_fields = ['research_id']  

        
class ResearchArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Research_articles
        fields = ['title', 'description', 'link', 'admin_id']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()

    def validate_description(self, value):
        if not value.strip():
            raise serializers.ValidationError("Description cannot be empty.")
        if len(value) > 10000:
            raise serializers.ValidationError("Description cannot exceed 10,000 characters.")
        return value.strip()

    def validate_link(self, value):
        if not value.strip():
            raise serializers.ValidationError("Link cannot be empty.")
        return value.strip()
