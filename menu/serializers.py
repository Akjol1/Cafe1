import django_filters
from rest_framework import serializers
from rest_framework import filters

from .models import Category, Rating, Menu, Comment, Like
from django.db.models import Avg


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        comment = Comment.objects.create(author=user, **validated_data)
        return comment

    class Meta:
        model = Comment
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title', 'category']
    search_fields = ['created_at']

    class Meta:
        model = Menu
        fields = '__all__'

    def validate_title(self, title):
        if self.Meta.model.objects.filter(title=title).exists():
            raise serializers.ValidationError('Такой заголовок уже существует')
        return title

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        tags = validated_data.pop('tags', [])
        menu = Menu.objects.create(author=user, **validated_data)
        menu.tags.add(*tags)
        return menu

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comments'] = CommentSerializer(
            Comment.objects.filter(post=instance.pk),
            many=True
        ).data
        representation['rating'] = instance.rating.aggregate(Avg('rating'))['rating__avg']
        # queryset = Like.objects.filter(is_liked=True)
        representation['likes_count'] = instance.likes.count()

        return representation


class RatingSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')

    class Meta:
        model = Rating
        fields = ['id', 'rating', 'author', 'post']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        rating = Rating.objects.create(author=user, **validated_data)
        return rating

    def validate_rating(self, rating):
        if rating not in range(1, 6):
            raise serializers.ValidationError(
                'Рейтинг должен быть от 1 до 5'
            )
        return rating

    def update(self, instance, validated_date):
        instance.rating = validated_date.get(
            'rating'
        )
        instance.save()
        return super().update(instance, validated_date)


class LikeSerializer(serializers.ModelSerializer):
    product = serializers.ReadOnlyField()

    class Meta:
        model = Like
        fields = "__all__"