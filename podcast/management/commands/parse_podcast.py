from django.core.management.base import BaseCommand
from podcast.parser import PodcastParser, PodcastDataSaver
from podcast.models import PodcastLink


class Command(BaseCommand):
    help = "Parse and update podcast data"

    def handle(self, *args, **options):
        podcast_links = PodcastLink.objects.all()

        for link in podcast_links:
            rss_feed_url = link.url
            parser = PodcastParser(rss_feed_url)
            podcast_data = parser.parse()

            if podcast_data:
                podcast_title = link.title

                saver = PodcastDataSaver(podcast_data)
                saver.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully parsed and updated podcast data for '{podcast_title}' ({rss_feed_url})"
                    )
                )
            else:
                self.stderr.write(
                    self.style.ERROR(
                        f"Error parsing the podcast data for {rss_feed_url}"
                    )
                )
