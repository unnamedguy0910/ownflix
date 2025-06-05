from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


def user_directory_path(instance, filename):
    # This function determines the upload path for user files
    return f'user_{instance.room.created_by.id}/room_{instance.room.id}/{filename}'



class Room(models.Model):
    slug = models.SlugField(unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    youtube_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.slug


class Video(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='videos')
    file = models.FileField(upload_to='videos/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.room.slug})"


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.sender.username} @ {self.room.slug} [{self.timestamp.strftime('%H:%M:%S')}]"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
