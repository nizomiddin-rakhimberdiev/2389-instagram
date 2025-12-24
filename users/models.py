from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, unique=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/def_avatar.png')
    bio = models.CharField(max_length=150)


class Chat(models.Model):
    participants = models.ManyToManyField(CustomUser)
    updated_at = models.DateTimeField(auto_now=True)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
