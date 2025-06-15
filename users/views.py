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
    
    # Return errors if serializer is invalid
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
                'lname' : user.email,
                'email' : user.email,
                'full_name' : user.full_name,
                'is_staff' : user.is_staff,
            },
            'tokens' : tokens
        }, status = status.HTTP_200_OK)
    
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    # this is used to get the user profile information

    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data , status = status.HTTP_200_OK)



@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_profile(request):
    # this is to update the user profile

    serializer = UserProfileSerializer(request.user, data = request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
    'message': 'Profile updated successfully',
    'user': serializer.data
}, status=status.HTTP_200_OK)

    
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_user(request):
    # this is a user logout endpoint which will blacklist the refresh token
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
