from rest_framework import serializers
from .models import Gallery_images
from admin_actions.models import Admin

class GalleryImageSerializer(serializers.ModelSerializer):
    admin_username = serializers.CharField(source='admin_id.username', read_only=True)
    image_id = serializers.CharField(read_only=True) 
    
    class Meta:
        model = Gallery_images
        fields = ['image_id', 'uploaded_at', 'image', 'caption', 'admin_id', 'admin_username']
        read_only_fields = ['uploaded_at', 'image_id'] 
    
    def validate_admin_id(self, value):
        if not Admin.objects.filter(admin_id=value.admin_id).exists():
            raise serializers.ValidationError("Admin does not exist.")
        return value

class GalleryImageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery_images
        fields = ['caption', 'image']
        
    def validate_image(self, value):
        if value:
            if value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError("Image file size should not exceed 5MB.")
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/jpg']
            if hasattr(value, 'content_type') and value.content_type not in allowed_types:
                raise serializers.ValidationError("Only JPEG, JPG, PNG, GIF, and WebP images are allowed.")
        
        return value