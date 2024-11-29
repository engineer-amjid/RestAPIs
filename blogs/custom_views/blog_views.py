from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import BlogPost
from ..serializers.blog_post_serializer import BlogPostSerializer
from blogs.shared.utils import custom_response  # Import the utility function


class BlogPostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return custom_response(
            message="Blog post created successfully",
            status_code=status.HTTP_201_CREATED,
            data=serializer.data
        )

    def list(self, request, *args, **kwargs):
        """
        Retrieve all blog posts with custom response.
        """
        # Get all blog posts
        blog_posts = self.get_queryset()
        serializer = self.get_serializer(blog_posts, many=True)

        # Prepare response
        return custom_response(
            message="Blog posts retrieved successfully",
            status_code=status.HTTP_200_OK,
            data=serializer.data
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return custom_response(
            message="Blog post retrieved successfully",
            status_code=status.HTTP_200_OK,
            data=serializer.data
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return custom_response(
            message="Blog post updated successfully",
            status_code=status.HTTP_200_OK,
            data=serializer.data
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return custom_response(
            message="Blog post deleted successfully",
            status_code=status.HTTP_204_NO_CONTENT,
            data=None
        )