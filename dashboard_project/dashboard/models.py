from django.db import models
from django.contrib.auth.models import User

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    # Add other fields as needed for the user profile

    def __str__(self):
        return self.user.username
    
class ActivityLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.timestamp} - {self.user.username} - {self.action}"

class Analytics(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    page = models.CharField(max_length=255)
    views = models.IntegerField(default=0)
    unique_views = models.IntegerField(default=0)