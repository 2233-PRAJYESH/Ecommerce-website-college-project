from django.contrib import admin
from .models import Chat, Message, GroupChat, GroupMessage, Relationship

# Register your models here.
admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(GroupChat)
admin.site.register(GroupMessage)
admin.site.register(Relationship)