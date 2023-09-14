from django.http import Http404
from rest_framework import generics
from .models import Podcast, PodcastEpisode
from rest_framework.pagination import PageNumberPagination
from .serializers import PodcastSerializer, PodcastEpisodeSerializer


class PodcastListCreateView(generics.ListCreateAPIView):
    serializer_class = PodcastSerializer

    def get_queryset(self):
        queryset = Podcast.objects.all()
        return queryset

