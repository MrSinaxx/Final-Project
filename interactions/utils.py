from django.db.models import Count
from .models import PodcastEpisode, Like


from podcast.models import PodcastEpisode, Podcast


from podcast.models import PodcastEpisode, Podcast


def get_content_recommendations(user):
    # Step 1: Collect Liked Genres for the User
    liked_genres = user.like_set.values_list(
        "podcast_episode__podcast__genres", flat=True
    ).distinct()

    # Step 2: Find Podcasts with Liked Genres
    matching_podcasts = Podcast.objects.filter(genres__in=liked_genres).distinct()

    recommendations = []

    # Step 3: Retrieve Latest Episodes for Matched Podcasts
    for podcast in matching_podcasts:
        latest_episodes = PodcastEpisode.objects.filter(podcast=podcast).order_by(
            "-publish_date"
        )[:10]
        recommendations.extend(latest_episodes)

    return recommendations
