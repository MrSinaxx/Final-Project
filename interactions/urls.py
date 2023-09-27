from django.urls import path
from .views import (
    LikePodcastEpisodeAPIView,
    CommentPodcastEpisodeAPIView,
    SavePodcastEpisodeAPIView,
    UnlikePodcastEpisodeAPIView,
    UnsavePodcastEpisodeAPIView,
    ListLikedPodcastEpisodesAPIView,
    ListSavedPodcastEpisodesAPIView,
    UserReadItemsAPIView,
    RecommendationsAPIView,
)

urlpatterns = [
    path(
        "like/<int:episode_id>/",
        LikePodcastEpisodeAPIView.as_view(),
        name="like-podcast-episode",
    ),
    path(
        "unlike/<int:episode_id>/",
        UnlikePodcastEpisodeAPIView.as_view(),
        name="unlike-podcast-episode",
    ),
    path(
        "comment/<int:episode_id>/",
        CommentPodcastEpisodeAPIView.as_view(),
        name="comment-podcast-episode",
    ),
    path(
        "save/<int:episode_id>/",
        SavePodcastEpisodeAPIView.as_view(),
        name="save-podcast-episode",
    ),
    path(
        "unsave/<int:episode_id>/",
        UnsavePodcastEpisodeAPIView.as_view(),
        name="unsave-podcast-episode",
    ),
    path(
        "liked-episodes/",
        ListLikedPodcastEpisodesAPIView.as_view(),
        name="list-liked-podcast-episodes",
    ),
    path(
        "saved-episodes/",
        ListSavedPodcastEpisodesAPIView.as_view(),
        name="list-saved-podcast-episodes",
    ),
    path("read-items/", UserReadItemsAPIView.as_view(), name="user-read-items"),
    path("recommendations/", RecommendationsAPIView.as_view(), name="recommendations"),
]
