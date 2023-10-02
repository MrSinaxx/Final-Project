from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import SavedPodcast, PodcastEpisode, Like, Viewed
from .serializers import LikeSerializer, CommentSerializer, SavedPodcastSerializer
from podcast.serializers import PodcastEpisodeSerializer
from interactions.utils import (
    get_content_recommendations,
)


class LikePodcastEpisodeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, episode_id):
        episode = PodcastEpisode.objects.get(id=episode_id)
        like, created = Like.objects.get_or_create(
            user=request.user, podcast_episode=episode
        )

        if created:
            serializer = LikeSerializer(like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"message": "Podcast episode already liked"}, status=status.HTTP_200_OK
            )


class UnlikePodcastEpisodeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, episode_id):
        episode = PodcastEpisode.objects.get(id=episode_id)
        try:
            like = Like.objects.get(user=request.user, podcast_episode=episode)
            like.delete()
            return Response(
                {"message": "Podcast episode unliked"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Like.DoesNotExist:
            return Response(
                {"message": "You have not liked this podcast episode"},
                status=status.HTTP_404_NOT_FOUND,
            )


class CommentPodcastEpisodeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, episode_id):
        episode = PodcastEpisode.objects.get(id=episode_id)
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user, podcast_episode=episode)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SavePodcastEpisodeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, episode_id):
        episode = PodcastEpisode.objects.get(id=episode_id)
        serializer = SavedPodcastSerializer(data={"podcast_episode": episode.id})

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {"message": "Podcast episode saved"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnsavePodcastEpisodeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, episode_id):
        episode = PodcastEpisode.objects.get(id=episode_id)
        try:
            saved_podcast = SavedPodcast.objects.get(
                user=request.user, podcast_episode=episode
            )
            saved_podcast.delete()
            return Response(
                {"message": "Podcast episode unsaved"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except SavedPodcast.DoesNotExist:
            return Response(
                {"message": "You have not saved this podcast episode"},
                status=status.HTTP_404_NOT_FOUND,
            )


class ListLikedPodcastEpisodesAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        liked_episodes = Like.objects.filter(user=request.user).values_list(
            "podcast_episode", flat=True
        )
        podcast_episodes = PodcastEpisode.objects.filter(id__in=liked_episodes)
        serializer = PodcastEpisodeSerializer(podcast_episodes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListSavedPodcastEpisodesAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        saved_episodes = SavedPodcast.objects.filter(user=request.user).values_list(
            "podcast_episode", flat=True
        )
        podcast_episodes = PodcastEpisode.objects.filter(id__in=saved_episodes)
        serializer = PodcastEpisodeSerializer(podcast_episodes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserReadItemsAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PodcastEpisodeSerializer

    def get_queryset(self):
        user = self.request.user

        viewed_episodes = Viewed.objects.filter(user=user).values_list(
            "podcast_episode", flat=True
        )
        queryset = PodcastEpisode.objects.filter(id__in=viewed_episodes)

        return queryset


class RecommendationsAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PodcastEpisodeSerializer

    def get(self, request):
        user = request.user
        recommendations = get_content_recommendations(user)[:10]
        serializer = self.serializer_class(recommendations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
