from django.db import models

class UserProfile(models.Model):
    # Fields for the user profile
    username = models.CharField(max_length=50, unique=True)
    instagram = models.URLField(blank=True)  # URLs can be empty
    twitter = models.URLField(blank=True)  # URLs can be empty
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.username
