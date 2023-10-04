from celery import shared_task, Task
from celery.utils.log import get_task_logger
from podcast.parser import PodcastParser, PodcastDataSaver
from podcast.models import PodcastLink

logger = get_task_logger(__name__)


class RetryTask(Task):
    autoretry_for = (Exception, KeyError)
    retry_kwargs = {"max_retries": 5}
    retry_backoff = 2


@shared_task(bind=True, base=RetryTask)
def scrape_and_update_podcast(self, podcast_link_id):
    try:
        link = PodcastLink.objects.get(id=podcast_link_id)
        rss_feed_url = link.url

        parser = PodcastParser(rss_feed_url)
        podcast_data = parser.parse()

        if podcast_data:
            podcast_title = link.title
            saver = PodcastDataSaver(podcast_data)
            saver.save()
            logger.info(
                f"Successfully parsed and updated podcast data for '{podcast_title}' ({rss_feed_url})"
            )
        else:
            logger.error(f"Error parsing the podcast data for {rss_feed_url}")

    except PodcastLink.DoesNotExist:
        logger.error(f"PodcastLink with id {podcast_link_id} does not exist")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise self.retry(exc=e)
