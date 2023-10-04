from django.core.management.base import BaseCommand
from podcast.models import PodcastLink
from podcast.tasks import scrape_and_update_podcast


class Command(BaseCommand):
    help = "Parse and update podcast data"

    def handle(self, *args, **options):
        podcast_links = PodcastLink.objects.all()

        for link in podcast_links:
            scrape_and_update_podcast.delay(link.id)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Enqueued scraping task for '{link.title}' ({link.url})"
                )
            )
