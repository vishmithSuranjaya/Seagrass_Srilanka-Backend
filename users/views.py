from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from .models import Users
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model

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

# List all users (admin only)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def list_all_users(request):
    users = Users.objects.all()
    serializer = UserProfileSerializer(users, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
def admin_update_user(request, user_id):
    try:
        user = Users.objects.get(user_id=user_id)
    except Users.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if 'is_staff' in request.data:
        if not request.user.is_superuser:
            return Response({'error': 'Only the website owner can change admin status.'}, status=status.HTTP_403_FORBIDDEN)

        if user.is_superuser and user == request.user:
            return Response({'error': 'Cannot remove admin rights from the website owner.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserProfileSerializer(user, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User updated successfully', 'user': serializer.data}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Admin: delete any user
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_delete_user(request, user_id):
    try:
        user = Users.objects.get(user_id=user_id)
    except Users.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    user.delete()
    return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)

# Admin: deactivate or activate any user
@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def admin_toggle_active_user(request, user_id):
    try:
        user = Users.objects.get(user_id=user_id)
    except Users.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    is_active = request.data.get('is_active')
    if is_active is None:
        return Response({'error': 'is_active field is required'}, status=status.HTTP_400_BAD_REQUEST)
    # Robustly convert is_active to boolean
    if isinstance(is_active, bool):
        user.is_active = is_active
    elif isinstance(is_active, str):
        user.is_active = is_active.lower() in ['true', '1', 'yes']
    elif isinstance(is_active, int):
        user.is_active = bool(is_active)
    else:
        return Response({'error': 'Invalid is_active value'}, status=status.HTTP_400_BAD_REQUEST)
    user.save()
    return Response({'message': f'User {"activated" if user.is_active else "deactivated"} successfully', 'is_active': user.is_active}, status=status.HTTP_200_OK)

# Superuser: create admin user
@api_view(['POST'])
@permission_classes([IsAdminUser])
def superuser_create_admin_user(request):
    if not request.user.is_superuser:
        return Response({'error': 'Only the website owner (superuser) can create admin accounts.'}, status=status.HTTP_403_FORBIDDEN)
    data = request.data.copy()
    data['is_staff'] = True
    serializer = UserRegistrationSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'message': 'Admin user created successfully', 'user': UserProfileSerializer(user).data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from .models import Users
from django.contrib.auth.hashers import check_password

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


# @api_view(['PUT', 'PATCH'])
# @permission_classes([permissions.IsAuthenticated])
# def update_profile(request):
#     # this is to update the user profile

#     serializer = UserProfileSerializer(request.user, data = request.data, partial=True, context={'request': request})
#     if serializer.is_valid():
#         serializer.save()
#         return Response({
#     'message': 'Profile updated successfully',
#     'user': serializer.data
# }, status=status.HTTP_200_OK)

    
#     return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)@api_view(['PUT', 'PATCH'])
@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_profile(request, user_id):
    try:
        user_instance = Users.objects.get(user_id=user_id)
    except Users.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Ensure only the owner (by matching IDs) or admin can update
    if str(request.user.user_id) != str(user_instance.user_id) and not request.user.is_staff:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    serializer = UserProfileSerializer(
        user_instance,
        data=request.data,
        # files=request.FILES, 
        partial=True,
        context={'request': request}
    )
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                'message': 'Profile updated successfully',
                'user': serializer.data
            },
            status=status.HTTP_200_OK
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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

#to change the password
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password(request, user_id):
    user = request.user

    # Optional: ensure only the user themselves can change their password
    if str(user.user_id) != str(user_id):
        return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')

    if not current_password or not new_password:
        return Response({'error': 'Both current and new password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Verify current password
    if not check_password(current_password, user.password):
        return Response({'error': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

    # Set new password
    user.set_password(new_password)
    user.save()

    return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
