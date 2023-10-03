from rest_framework import serializers
from .models import Comment, SavedPodcast, Like


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class SavedPodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedPodcast
        exclude = ("user",)  # Exclude the 'user' field from serialization


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"