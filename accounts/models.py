from django.db import models

# Create your models here.
class UserProfile(models.Model):
    username = models.CharField(max_length = 20)
    email = models.EmailField(max_length = 20)
    password = models.CharField(max_length = 20)
    created_at = models.DateTimeField(auto_now_add = True)
    
