from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tasks",default=1)
    
    assigned_to = models.ManyToManyField(User, related_name='assigned_tasks')

    title = models.CharField(max_length=255)

    # Status of the task # completed = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    # Timestamp when task is created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Extending Djangos default user model : by creating a user profile (1 on 1 relationship)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    
    def __str__(self):
        return self.user.username
