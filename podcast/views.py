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


class PodcastDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PodcastSerializer

    def get_object(self):
        pk = self.kwargs["pk"]

        queryset = Podcast.objects.filter(pk=pk)

        if not queryset.exists():
            raise Http404("Podcast not found")

        return queryset.first()


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000


class PodcastEpisodeListCreateView(generics.ListCreateAPIView):
    serializer_class = PodcastEpisodeSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        podcast_pk = self.kwargs["pk"]

        queryset = PodcastEpisode.objects.filter(podcast__pk=podcast_pk)

        if not queryset.exists():
            raise Http404("Podcast episode not found")

        return queryset
