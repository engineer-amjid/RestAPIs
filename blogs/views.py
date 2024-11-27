from django.contrib.auth.models import User
from rest_framework import viewsets, generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import BlogPost
from .serializers.blog_post_serializer import BlogPostSerializer
from .serializers.user_serializer import UserSerializer


class RegisterUserViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # Serialize the data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the user
        user = serializer.save()

        # Create a token for the user
        token = Token.objects.create(user=user)

        # Prepare the response data
        response_data = {
            'message': 'User created successfully',
            'status': 'success',
            'data': {
                'token': token.key,
                'user': UserSerializer(user, context=self.get_serializer_context()).data
            },
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class LoginUserViewSet(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data = request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'message': 'Login successful',
            'status': 'success',
            'data': {
                'token': token.key,
                'user': UserSerializer(user, context=self.get_serializer_context()).data
            },
        })

class BlogPostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

