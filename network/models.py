from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Fallower(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="to_fallow")
    fallowers = models.ManyToManyField("User", related_name="fallower_list")
    fallowing = models.ManyToManyField("User", related_name="fallowing_list")

    def __str__(self):
        return f" {self.id} {self.user} Fallow"

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "user_id": self.user.id,
            "fallowers": [user.username for user in self.fallowers.all()],
            "fallowing": [user.username for user in self.fallowing.all()],

        }


class Post(models.Model):
    author = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="posted_by")
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default='0')
    body = models.TextField(max_length=100)
    liked_by = models.ManyToManyField(User, related_name='posts')

    def __str__(self):
        return f" {self.id} {self.author} Posted at {self.timestamp}"

    def serialize(self):
        return {
            "id": self.id,
            'author_id': self.author.id,
            "author": self.author.username,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes,
            "liked_by": [user.username for user in self.liked_by.all()]

        }
