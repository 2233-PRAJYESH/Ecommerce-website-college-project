from django.db import models
from django.contrib.auth.models import User
from store.models import Product

class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name="user_groups", blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_groups")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class GroupProductShare(models.Model):
    group = models.ForeignKey("groups.Group", on_delete=models.CASCADE, related_name="shared_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} shared in {self.group.name}"


class Feedback(models.Model):
    group_share = models.ForeignKey(GroupProductShare, on_delete=models.CASCADE, related_name="feedbacks")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username} on {self.group_share.product.name}"
