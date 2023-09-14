from django.core.management.base import BaseCommand
from podcast.parser import parse_rss_feed, save_podcast_data_to_db


class Command(BaseCommand):
    help = "Parse and update podcast data"

    def handle(self, *args, **options):
        rss_feed_url = "https://rss.art19.com/apology-line"

        podcast_data = parse_rss_feed(rss_feed_url)
        save_podcast_data_to_db(podcast_data)

        if podcast_data:
            self.stdout.write(
                self.style.SUCCESS("Successfully parsed and updated podcast data")
            )
        else:
            self.stderr.write(self.style.ERROR("Error parsing the podcast data"))
