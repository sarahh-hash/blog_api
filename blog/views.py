from rest_framework import status
from rest_framework.response import Response
from django.db import models
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied

from .models import Post, Comment
from .serializers import (
    RegisterSerializer,
    PostSerializer,
    PostDetailSerializer,
    PostValidateSerializer,
    CommentSerializer,
    CommentValidateSerializer
)
from .permissions import (
    IsAuthorOrReadOnly,
    IsCommentAuthorOrReadOnly
)


class TotalPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


class RegisterView(ListCreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    queryset = []


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    pagination_class = TotalPagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            return Post.objects.filter(
                models.Q(is_published=True) | models.Q(author=user)
            ).distinct()

        return Post.objects.filter(is_published=True)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PostValidateSerializer

        if self.action == 'retrieve':
            return PostDetailSerializer

        return PostSerializer


class PostCommentsView(ListCreateAPIView):
    serializer_class = CommentSerializer
    pagination_class = TotalPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        post_id = self.kwargs['post_id']

        return Comment.objects.filter(
            post_id=post_id,
            is_approved=True
        )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentValidateSerializer

        return CommentSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['post'] = Post.objects.get(id=self.kwargs['post_id'])
        return context

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs['post_id'])

        if not post.is_published:
            raise PermissionDenied('Cannot comment on unpublished post.')

        serializer.save()


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthorOrReadOnly]
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CommentValidateSerializer

        return CommentSerializer

class CommentDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticated,
        IsCommentAuthorOrReadOnly
    ]
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CommentValidateSerializer

        return CommentSerializer