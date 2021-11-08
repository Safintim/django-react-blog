from rest_framework.viewsets import ModelViewSet

from blog.models import Post
from blog.serializers import PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects
    serializer_class = PostSerializer
