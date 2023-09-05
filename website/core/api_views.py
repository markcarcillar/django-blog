from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from .models import BlogModel, LikeModel
from .serializers import LikeToggleSerializer
from .models import CommentModel
from .serializers import CommentSerializer


class LikeToggleAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = LikeToggleSerializer(data=request.data)
        if serializer.is_valid() and request.user.is_authenticated:
            blog_id = serializer.validated_data['blog_id']
            blog = get_object_or_404(BlogModel, id=blog_id)
            user = request.user

            # Toggle like/unlike
            liked, created = LikeModel.objects.get_or_create(blog=blog, user=user)
            if not created:
                liked.delete()
                return Response({'message': 'Unliked', 'likes_count': blog.likemodel_set.count()}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Liked', 'likes_count': blog.likemodel_set.count()}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentCreateAPI(APIView):
    
    def post(self, request, blog_id):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response({'message': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

        # Get the associated blog
        blog = get_object_or_404(BlogModel, pk=blog_id)

        # Create a Comment instance
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(blog=blog, user=request.user)
            return Response({'message': 'Comment created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
