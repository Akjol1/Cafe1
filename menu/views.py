import django_filters
from django.shortcuts import render
from django_filters import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from .models import Category, Comment, Like, Menu, Rating
from .permissions import IsAdminAuthPermission, IsAuthorPermission
from .serializers import CategorySerializer, CommentSerializer, LikeSerializer, RatingSerializer, MenuSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]

        elif self.action == 'create':
            self.permission_classes = [IsAdminAuthPermission]

        elif self.action in ['update', 'partial_update', 'destroy']:
                self.permission_classes = [IsAuthorPermission]

        return super().get_permissions()


class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]

        elif self.action == 'create':
            self.permission_classes = [IsAdminAuthPermission]

        elif self.action in ['update', 'partial_update', 'destroy']:
                self.permission_classes = [IsAuthorPermission]

        return super().get_permissions()


class MenuViewSet(ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filterset_fields = ['category']
    search_fields = ['created_at']
    ordering_fields = ['created_at', 'title']

    @action(['GET'], detail=True)
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(['POST', 'PATCH'], detail=True)
    def rating(self, request, pk=None):
        data = request.data.copy()
        data['post'] = pk
        serializer = RatingSerializer(
            data=data, context={'request': request}
        )
        rating = Rating.objects.filter(
            author=request.user,
            post=pk
        ).first()
        if serializer.is_valid(raise_exception=True):
            if rating and request.method == 'POST':
                return Response('use PATCH method')
        elif rating and request.method == 'PATCH':
            serializer.update(rating, serializer.validated_data)
            return Response('UPDATED')
        elif request.method == 'POST':
            serializer.create(
                serializer.validated_data
            )
            return Response('CREATED')

    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(post=post, author=user)
            like.is_liked = not like.is_liked
            like.save()
            message = 'liked' if like.is_liked else 'disliked'
            if not like.is_liked:
                like.delete()
        except Like.DoesNotExist:
            Like.objects.create(post=post, author=user, is_liked=True)
            message = 'liked'
        return Response(message, status=200)

    def get_serializer_class(self):
        if self.action == 'list':
            return Menu
        return self.serializer_class

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]

        elif self.action == 'create':
            self.permission_classes = [IsAdminAuthPermission]

        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorPermission]

        return super().get_permissions()