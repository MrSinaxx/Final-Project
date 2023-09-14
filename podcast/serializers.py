from rest_framework import serializers
from .models import Podcast, PodcastEpisode, PodcastLink


class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = [
            "title",
            "summary",
            "subtitle",
            "authorName",
            "imageUrl",
            "rssOwnerName",
            "rssOwnerPublicEmail",
            "websiteUrl",
            "isExplicitContent",
            "copyright",
            "language",
            "contentType",
            "genres",
        ]


class PodcastEpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PodcastEpisode
        fields = [
            "podcast",
            "title",
            "duration",
            "audioUrl",
            "publish_date",
            "explicit",
            "imageUrl",
            "summary",
            "description",
        ]


