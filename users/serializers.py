from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import Users  

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ('fname', 'lname', 'email', 'password', 'password_confirm')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = Users.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)

            if not user:
                raise serializers.ValidationError("Invalid credentials.")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
            attrs['user'] = user
        else:
            raise serializers.ValidationError("Email and password must be included.")
        return attrs

from rest_framework import serializers
from .models import Users

class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    is_staff = serializers.BooleanField(read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = (
            'user_id', 'fname', 'lname', 'email',
            'full_name', 'date_joined', 'is_staff', 'image',
            'is_active', 'is_superuser', 'last_login',
        )
        read_only_fields = ('user_id', 'date_joined', 'is_staff', 'is_superuser', 'last_login')

    def get_full_name(self, obj):
        return f"{obj.fname} {obj.lname}".strip()

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

    def validate_image(self, value):
        if value:
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError("Image file too large. Size should not exceed 5MB.")

            allowed_types = ['image/jpeg', 'image/png', 'image/gif']
            if hasattr(value, 'content_type') and value.content_type not in allowed_types:
                raise serializers.ValidationError("Invalid image format. Only JPEG, PNG, and GIF are allowed.")

        return value

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and not request.user.is_superuser:
            validated_data.pop('is_staff', None)
            validated_data.pop('is_superuser', None)  # extra safety
        return super().update(instance, validated_data)
