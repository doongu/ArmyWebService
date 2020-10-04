from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    nickname = models.CharField(max_length=100)

class Online(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    channel_name = models.TextField()
    time = models.DateTimeField()

class Dialog(models.Model):
    counselee = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='dialogs',
        related_query_name='dialog'
    )
    time = models.DateTimeField()

class Chat(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='chats',
        related_query_name='chat'
    )
    dialog = models.ForeignKey(
        Dialog,
        on_delete=models.PROTECT,
        related_name='chats',
        related_query_name='chat')
    message = models.TextField()
    time = models.DateTimeField()