from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from store.models import Product  # Adjust if needed

class Group(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_groups')
    members = models.ManyToManyField(User, related_name='member_groups')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class GroupProductShare(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    share = models.ForeignKey(GroupProductShare, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_useful = models.BooleanField()
    comment = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
