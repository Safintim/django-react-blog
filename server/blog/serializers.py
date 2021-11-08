from rest_framework.serializers import ModelSerializer

from blog.models import Post


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'text')
        read_only_fields = ('id',)
