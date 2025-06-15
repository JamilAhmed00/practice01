from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  RegisterView, UserDetailView, TagViewSet, TaskViewSet

router = DefaultRouter()
router.register('tasks', TaskViewSet, basename='task')
router.register('tags', TagViewSet, basename='tag')

urlpatterns = [
    
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserDetailView.as_view(), name='users'),
    path('', include(router.urls))
]

