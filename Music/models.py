from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    name = models.CharField(max_length=255, blank=True, null=True)
    favorite_songs = models.ManyToManyField('Songs', related_name='favorited_by', blank=True)

    def __str__(self):
        return self.username

class Album(models.Model):
    name = models.CharField(max_length=100, default='Default Album Name')

    def __str__(self):
        return self.name

class Artist(models.Model):
    name = models.CharField(max_length=20)
    singer_image = models.ImageField(upload_to='singer_images', null=True, blank=True)

    def __str__(self):
        return self.name

class Songs(models.Model):
    LANGUAGE_CHOICES = (
        ('Hindi', 'Hindi'),
        ('English', 'English'),
        ('Telugu', 'Telugu'),
        ('Tamil', 'Tamil'),
    )

    title = models.CharField(max_length=100, default='Untitled')
    song_file = models.FileField(upload_to='songs')
    image = models.FileField(upload_to='song_images')
    artist = models.ForeignKey(Artist, related_name='songs', on_delete=models.CASCADE, null=True)
    singer = models.CharField(max_length=200)
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='Telugu')

    def __str__(self):
        return self.title
