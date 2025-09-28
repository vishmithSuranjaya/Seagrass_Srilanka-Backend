from rest_framework import serializers
from .models import Blog, Comments, Likes

class CommentSerializer(serializers.ModelSerializer):
    author_full_name = serializers.SerializerMethodField()
    author_image = serializers.SerializerMethodField()
    blog_title = serializers.CharField(source="blog_id.title",read_only=True)
    
    class Meta:
        model = Comments
        fields = '__all__'

    def get_author_full_name(self, obj):
        return f"{obj.user_id.fname} {obj.user_id.lname}"
    
    def get_author_image(self, obj):
        request = self.context.get('request')
        if obj.user_id.image:
            if request:
                return request.build_absolute_uri(obj.user_id.image.url)
            return obj.user_id.image.url
        return None



class BlogSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    user_has_liked = serializers.SerializerMethodField()
    user_fname = serializers.SerializerMethodField()
    user_lname = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'blog_id',
            'title',
            'content',
            'image',
            'image_url',
            'like_count',
            'date',
            'time',
            'status',
            'user_id',
            'user_fname',
            'user_lname',
            'comment_id',
            'comments',
            'user_has_liked',
        ]
    def get_user_fname(self, obj):
        return obj.user_id.fname if obj.user_id else ''

    def get_user_lname(self, obj):
        return obj.user_id.lname if obj.user_id else ''

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def get_comments(self, obj):
        comments = Comments.objects.filter(blog_id=obj.blog_id)
        return CommentSerializer(comments, many=True, context=self.context).data

    def get_user_has_liked(self, obj):
        request = self.context.get('request')
        user = request.user if request else None
        if user and user.is_authenticated:
            return Likes.objects.filter(blog=obj, user=user).exists()
        return False