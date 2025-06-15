from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserRegisterSerializer
from rest_framework import viewsets, permissions
from .models import Task,Tag
from .serializers import TaskSerializer, TagSerializer, UserSerializer
from .permissions import IsOwner
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from django.db import models
from rest_framework.response import Response


#from django.db.models import Q
from rest_framework.exceptions import PermissionDenied


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


import environ
import os

env = environ.Env()
environ.Env.read_env(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

my_secret = env('a')
print(my_secret)  # This will print the value of 'a' from your .env file

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    #parser_classes = [MultiPartParser, FormParser]
    
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    parser_classes = [FormParser, MultiPartParser]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Task.objects.none()
        
        if self.request.user.is_superuser:
            return Task.objects.all()
        return Task.objects.filter(
            models.Q(user=self.request.user) |
            models.Q(assigned_to=self.request.user)
        ).distinct()
        
    def perform_create(self, serializer):
        assigned_to_ids = self.request.data.getlist('assigned_to') if 'assigned_to' in self.request.data else []

        if not self.request.user.is_superuser:
            if assigned_to_ids and any(str(uid) != str(self.request.user.id) for uid in assigned_to_ids):
                raise PermissionDenied("You are not allowed to assign tasks to other users.")
            task = serializer.save(user=self.request.user, assigned="self")
            if assigned_to_ids:
                task.assigned_to.set(assigned_to_ids)
        else:
            
            task = serializer.save(user=self.request.user, assigned="admin")
            task.assigned_to.set(assigned_to_ids)


    @action(detail=False, methods=['get'], url_path='assigned-to-me')
    def assigned_to_me(self, request):
        """
        Return all tasks assigned to the current user by an admin.
        """
        tasks = Task.objects.filter(assigned="admin", assigned_to=request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

   
    
    
        
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
        
  
    
class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user  
    
    
    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]