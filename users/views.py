from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from .models import Users

def get_token_for_user(user):
    #this will generate jwt tokens for the user 
    
    refresh = RefreshToken.for_user(user)
    return{
        'refresh' : str(refresh),
        'access' : str(refresh.access_token),

    }

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        tokens = get_token_for_user(user)
        
        return Response({
            'message': 'User Registered Successfully',
            'user': {
                'user_id': user.user_id,
                'fname': user.fname,
                'lname': user.lname,
                'email': user.email,
                'full_name': user.full_name,
            },
            'tokens': tokens
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    # this is a user login endpoint

    serializer = UserLoginSerializer(data= request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        tokens = get_token_for_user(user)
        
        return Response({
            'message' : 'Login successfull!',
            'user' : {
                'user_id' : user.user_id,
                'fname' : user.fname,
                'lname' : user.lname,
                'email' : user.email,
                'full_name' : user.full_name,
                'is_staff' : user.is_staff,
                'image': request.build_absolute_uri(user.image.url) if user.image else None,
            },
            'tokens' : tokens
        }, status = status.HTTP_200_OK)
    
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    # this is used to get the user profile information

    serializer = UserProfileSerializer(request.user, context={'request': request})
    return Response(serializer.data , status = status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_profile(request):
    # this is to update the user profile

    serializer = UserProfileSerializer(request.user, data = request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({
    'message': 'Profile updated successfully',
    'user': serializer.data
}, status=status.HTTP_200_OK)

    
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

#user's profile photo upload
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def upload_profile_image(request):
    
    if 'image' not in request.FILES:
        return Response({'error': 'No image file provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = UserProfileSerializer(request.user, data={'image': request.FILES['image']}, partial=True, context={'request': request})
    
    if serializer.is_valid():
        if request.user.image:
            try:
                request.user.image.delete(save=False)
            except:
                pass  
        
        serializer.save()
        return Response({
            'message': 'Profile image uploaded successfully',
            'image_url': serializer.data.get('image')
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#delete user profile picture
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_profile_image(request):  
    user = request.user
    if not user.image:
        return Response({'error': 'No profile image to delete'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user.image.delete(save=True)
        return Response({'message': 'Profile image deleted successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Failed to delete image'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# this is a user logout endpoint which will blacklist the refresh token
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_user(request):
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'message' : 'User Logged Out successfully'}, status = status.HTTP_200_OK)
        else:
            return Response({'error': 'Refresh Token is required' } , status = status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Invalid Token'}, status= status.HTTP_400_BAD_REQUEST)

# to get get any user(other functions allow to get logged in user only) details for blog,
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_user(request, user_id):
    try:
        user = Users.objects.get(user_id=user_id)
    except Users.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserProfileSerializer(user, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)