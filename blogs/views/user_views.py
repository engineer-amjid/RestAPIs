from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from ..models.profile_model import Profile
from ..serializers.user_serializer import UserSerializer
from ..serializers.profile_serializer import ProfileSerializer
from blogs.utils.utils import custom_response  # Import the utility function


class RegisterUserViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Serialize the data
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Save the user
            user = serializer.save()
            profile = Profile(user=user)
            profile.last_login = timezone.now()
            profile.save()

            # Create a token for the user
            token = Token.objects.create(user=user)

            # Prepare the response
            data = {
                'token': token.key,
                'profile': ProfileSerializer(profile, context=self.get_serializer_context()).data
            }
            return custom_response(
                message="User created successfully",
                status_code=status.HTTP_201_CREATED,
                data=data
            )

        except ValidationError as e:
            return custom_response(
                message="Validation error",
                status_code=status.HTTP_400_BAD_REQUEST,
                data=e.detail,
                success=False
            )

        except Exception as e:
            return custom_response(
                message="An error occurred during registration",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={'details': str(e)},
                success=False
            )

class LoginUserViewSet(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )

        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']

            # Ensure the profile exists or create one
            profile, created = Profile.objects.get_or_create(user=user)
            profile.last_login = timezone.now()
            profile.save()

            # Retrieve or create token
            token, created = Token.objects.get_or_create(user=user)

            # Prepare the response
            data = {
                'token': token.key,
                'profile': ProfileSerializer(profile, context=self.get_serializer_context()).data
            }
            return custom_response(
                message="Login successful",
                status_code=status.HTTP_200_OK,
                data=data
            )

        except ValidationError:
            return custom_response(
                message="Invalid credentials",
                status_code=status.HTTP_400_BAD_REQUEST,
                data={},
                success=False
            )

        except AuthenticationFailed:
            return custom_response(
                message="Authentication failed",
                status_code=status.HTTP_401_UNAUTHORIZED,
                data={},
                success=False
            )

        except Exception as e:
            return custom_response(
                message="An unexpected error occurred",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={'details': str(e)},
                success=False
            )
