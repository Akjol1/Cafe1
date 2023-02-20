from django.db import models
from slugify import slugify
from  django.contrib.auth import  get_user_model

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, primary_key=True, blank=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = 'Категории'


class Menu(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='menu')
    title = models.CharField(max_length=30)
    body = models.TextField()
    image = models.ImageField(upload_to='img/', blank=True)
    slug = models.SlugField(max_length=30, primary_key=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='menu')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = 'Категории'


class Rating(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='rating'

    )
    rating = models.PositiveSmallIntegerField()
    meny = models.ForeignKey(
        Menu, on_delete=models.CASCADE,
        related_name='rating'
    )

    def __str__(self):
        return f'{self.rating},-> {self.meny}'


class Comment(models.Model):
    body = models.CharField(max_length=30, )
    post = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.body


class Like(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='likes'
    )
    post = models.ForeignKey(
        Menu, on_delete=models.CASCADE,
        related_name='likes'
    )
    is_liked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.post}, Liked by {self.author.name}'
