from django.contrib import admin
from .models import Comment,Category,Like,Rating,Menu
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Menu)