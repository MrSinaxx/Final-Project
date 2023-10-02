from django.db import models
from django.contrib.auth.models import User
from podcast.models import PodcastEpisode
from django.conf import settings
from accounts.models import CustomUser


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    podcast_episode = models.ForeignKey(PodcastEpisode, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} likes {self.podcast_episode.title}"


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    podcast_episode = models.ForeignKey(PodcastEpisode, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.podcast_episode.title}"


class SavedPodcast(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    podcast_episode = models.ForeignKey(PodcastEpisode, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} saved {self.podcast_episode.title}"


class Viewed(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    podcast_episode = models.ForeignKey(PodcastEpisode, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} viewed {self.podcast_episode.title}"
