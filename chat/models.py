from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from django.core.exceptions import ValidationError

# Create your models here.
class AbstractMessage(models.Model):
    message_content = models.TextField(verbose_name="Message Content")
    sender = models.ForeignKey(User, verbose_name="Sender", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message_content
    
    class Meta:
        abstract = True
    
class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    user1 = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE, related_name="chat_user1")
    user2 = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE, related_name="chat_user2")
    # group_name = models.CharField(max_length=150)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user1', 'user2'], name='unique_relationship')
        ]

    def __str__(self):
        return str(self.id)
    
    def clean(self):
        if self.user1 == self.user2:
            raise ValidationError('User1 and User2 cannot be the same.')

class Message(AbstractMessage):
    chat_id = models.ForeignKey(Chat, verbose_name="Chat ID", on_delete=models.CASCADE)

    def __str__(self):
        return self.message_content

class GroupChat(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.TextField(max_length=50, null=False)
    relationship = models.ManyToManyField(User, through="Relationship")

    def __str__(self):
        return self.group_name

class Relationship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="User")
    group = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name="Group")

    def __str__(self):
        return f'{self.user.username} - {self.group.group_name}'

    class Meta:
        models.UniqueConstraint(fields=['user', 'group'], name='unique_relationship')

class GroupMessage(AbstractMessage):
    chat_id = models.ForeignKey(GroupChat, on_delete=models.CASCADE)

    def __str__(self):
        return self.message_content
    