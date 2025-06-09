from rest_framework import serializers
from .models import Research_articles

class ResearchArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Research_articles
        fields = '__all__'
