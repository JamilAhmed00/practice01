
from django.contrib.auth.models import User

from rest_framework import serializers
from .models import Task, Tag
import os ## ata validation add er jonno lage

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        
        
        
class TaskSerializer(serializers.ModelSerializer): 
    name = serializers.CharField(required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    is_done = serializers.BooleanField(required=False)
    file = serializers.FileField(required=False, allow_null=True)
    tag = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)
    assigned = serializers.CharField(read_only=True)
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, required=False)


    tag_names = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'name', 'start_date', 'end_date', 'is_done', 'tag', 'tag_names', 'user', 'file', 'assigned', 'assigned_to']
        read_only_fields = ['user', 'assigned']
        
    def validate_file(self, value):
        allowed_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.mp4']
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in allowed_extensions:
            raise serializers.ValidationError(f"Unsupported file extension '{ext}'. Allowed: {allowed_extensions}")
        return value

    def get_tag_names(self, obj):
        return [tag.name for tag in obj.tag.all()]



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'username']  # Prevent updating username
        
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user
