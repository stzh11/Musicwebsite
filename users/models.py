from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    avatar_image = models.ImageField(default='default_avatar.png', upload_to='avatars/')
    homepage_image = models.ImageField(default='default_homepage.png', upload_to='homepages/')

    def __str__(self):
        return self.username
