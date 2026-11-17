from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from .models import Post, Comment


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'password')

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(
        source='author.username',
        read_only=True
    )
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = 'id author title body is_published comments_count created_at updated_at'.split()

    def get_comments_count(self, post):
        return post.comments.filter(is_approved=True).count()


class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.CharField(
        source='author.username',
        read_only=True
    )
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = 'id author title body is_published comments created_at updated_at'.split()

    def get_comments(self, post):
        comments = post.comments.filter(is_approved=True)
        return CommentSerializer(comments, many=True).data


class PostValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, min_length=2)
    body = serializers.CharField()
    is_published = serializers.BooleanField(default=True)

    def create(self, validated_data):
        return Post.objects.create(
            author=self.context['request'].user,
            **validated_data
        )

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.is_published = validated_data.get(
            'is_published',
            instance.is_published
        )
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(
        source='author.username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = 'id post author body is_approved created_at updated_at'.split()
        read_only_fields = ('author', 'is_approved')


class CommentValidateSerializer(serializers.Serializer):
    body = serializers.CharField()

    def create(self, validated_data):
        return Comment.objects.create(
            post=self.context['post'],
            author=self.context['request'].user,
            **validated_data
        )

    def update(self, instance, validated_data):
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance