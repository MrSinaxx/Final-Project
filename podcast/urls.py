from django.urls import path
from .views import (
    PodcastListCreateView,
    PodcastDetailView,
    PodcastEpisodeListCreateView,
    PodcastEpisodeDetailView,
)

urlpatterns = [
    path("podcasts/", PodcastListCreateView.as_view(), name="podcast-list-create"),
    path("podcasts/<int:pk>/", PodcastDetailView.as_view(), name="podcast-detail"),
    path(
        "podcasts/<int:pk>/episodes/",
        PodcastEpisodeListCreateView.as_view(),
        name="podcast-episodes-list-create",
    ),
    path(
        "episodes/<int:pk>/",
        PodcastEpisodeDetailView.as_view(),
        name="podcast-episode-detail",
    ),
]
