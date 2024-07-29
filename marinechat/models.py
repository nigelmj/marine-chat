from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    def __str__(self):
        return self.username

class Document(models.Model):
    title = models.CharField(max_length=255, default="Untitled")
    file = models.FileField(upload_to="documents/")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    sender_choices = [
           ('user', 'User'),
           ('chatbot', 'Chatbot')
       ]
    sender = models.CharField(max_length=10, choices=sender_choices)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    references = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.message
