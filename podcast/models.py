from django.db import models


class Podcast(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField(max_length=255, null=True, blank=True)
    subtitle = models.CharField(max_length=100, null=True, blank=True)
    authorName = models.CharField(max_length=50, null=True)
    imageUrl = models.URLField(max_length=255, null=True, blank=True)
    rssOwnerName = models.CharField(max_length=50, null=True, blank=True)
    rssOwnerPublicEmail = models.EmailField(null=True, blank=True)
    websiteUrl = models.URLField(max_length=100, null=True, blank=True)
    isExplicitContent = models.CharField(max_length=3, default="no")
    copyright = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=2, null=True, blank=True)
    contentType = models.CharField(max_length=10, null=True, blank=True)
    genres = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.title


class PodcastEpisode(models.Model):
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)
    title = models.CharField(max_length=75)
    duration = models.CharField(max_length=25)
    audioUrl = models.URLField(max_length=300)
    publish_date = models.CharField(max_length=100)
    explicit = models.CharField(max_length=3, default="no")
    imageUrl = models.URLField(max_length=255, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
