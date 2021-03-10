from django.shortcuts import render

# Create your views here.
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from rest_framework.views import APIView
# from rest_framework import 

from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from tokenauth.serializers import UserSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    # def get(self, request, format=None):
    #     content = {
    #         'username': str(request.user),
    #         'user': str(request.user.email),  # `django.contrib.auth.User` instance.
    #         'token': str(request.auth),  # None
    #     }
    #     return Response(content)

# getting userlist################

    def get(self, request, format=None):
        """
        Return a list of all users.
        """

        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)
        
##############################
# class createView(APIView)
#     serializer_class=UserSerializer




class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })