
from django.urls import path, include
from .views import CategoryListView, MenuViewSet, CommentView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('menu/', MenuViewSet)
router.register('comments/', CommentView)


urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('', include(router.urls)),

]
