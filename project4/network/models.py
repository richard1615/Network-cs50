from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class user_description(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    description = models.TextField(blank=True, null=True) 

class posts(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=140)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField()

    def serialize(self):
        return {
            "likes":self.likes
        }

class PostLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_by")
    post = models.ForeignKey(posts, on_delete=models.CASCADE, related_name="liked")

class userFollowing(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following") # user following
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower") # user with follower


    class Meta:
        unique_together = ("follower", "following")
