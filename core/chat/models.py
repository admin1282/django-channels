from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_of_groups')
    members = models.ManyToManyField(User, related_name='groups_members')

class Message(models.Model):
    content = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)  # For personal chat
    timestamp = models.DateTimeField(auto_now_add=True)