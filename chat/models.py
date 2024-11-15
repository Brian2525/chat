from django.db import models

# models.py

import uuid
from django.db import models

class Visitor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class AssistantDescription(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Conversation(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    conversation_id = models.UUIDField(default=uuid.uuid4, editable=False, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Conversation {self.conversation_id} with {self.visitor.name}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=True)
    sender = models.CharField(max_length=10, choices=[('user', 'User'), ('assistant', 'Assistant')], null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.sender.capitalize()} at {self.timestamp}"







