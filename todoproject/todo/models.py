from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Task(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    tag = models.ManyToManyField(Tag, blank=False) 
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='media/', null=True, blank=True)  
    start_date = models.DateField()
    end_date = models.DateField()
    is_done = models.BooleanField(default=False)
    assigned = models.CharField(max_length=20, default='self')  # 'self' or 'admin'
    assigned_to = models.ManyToManyField(User, related_name='assigned_tasks', blank=True)  # assigned targets
    
    
    def __str__(self):
        return self.name