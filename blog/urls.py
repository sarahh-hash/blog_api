from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PostViewSet,
    PostCommentsView,
    CommentDetailAPIView
)


router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')


urlpatterns = [
    path('', include(router.urls)),

    path(
        'posts/<int:post_id>/comments/',
        PostCommentsView.as_view(),
        name='post-comments'
    ),

    path(
        'comments/<int:id>/',
        CommentDetailAPIView.as_view(),
        name='comment-detail'
    ),
]