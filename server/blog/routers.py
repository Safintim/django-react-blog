from rest_framework.routers import SimpleRouter

from blog.views import PostViewSet

router = SimpleRouter()
router.register('posts', PostViewSet, basename='posts')
