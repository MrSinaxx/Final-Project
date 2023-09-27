import xml.etree.ElementTree as ET
import requests
from django.db import transaction
from .models import Podcast, PodcastEpisode


class PodcastParser:
    def __init__(self, rss_url):
        self.rss_url = rss_url

    def parse(self):
        try:
            response = requests.get(self.rss_url)
            response.raise_for_status()
            xml_data = response.text
            return self.parse_xml(xml_data)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching RSS feed: {e}")
            return None

    def parse_xml(self, xml_data):
        podcast_metadata = {
            "title": "",
            "summary": "",
            "subtitle": "",
            "authorName": "",
            "imageUrl": "",
            "rssOwnerName": "",
            "rssOwnerPublicEmail": "",
            "websiteUrl": "",
            "isExplicitContent": "",
            "copyright": "",
            "language": "",
            "contentType": "",
            "genres": [],
        }

        episodes = []

        root = ET.fromstring(xml_data)

        for item in root.findall(".//item"):
            episode = {
                "title": item.findtext("title"),
                "duration": item.findtext(
                    "itunes:duration",
                    namespaces={"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"},
                ),
                "audioUrl": item.find("enclosure").get("url"),
                "publish_date": item.findtext("pubDate"),
                "explicit": item.findtext(
                    "itunes:explicit",
                    namespaces={"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"},
                ),
                "imageUrl": item.findtext(
                    "itunes:image",
                    namespaces={"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"},
                ),
                "summary": item.findtext(
                    "itunes:summary",
                    namespaces={"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"},
                ),
                "description": item.findtext(
                    ".//content:encoded",
                    namespaces={"content": "http://purl.org/rss/1.0/modules/content/"},
                ),
            }

            explicit_element = item.find(
                "itunes:explicit",
                namespaces={"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"},
            )
            if explicit_element is not None:
                episode["explicit"] = explicit_element.text
            else:
                episode["explicit"] = ""

            subtitle_element = item.find(
                "itunes:subtitle",
                namespaces={"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"},
            )
            if subtitle_element is not None:
                episode["subtitle"] = subtitle_element.text
            else:
                episode["subtitle"] = ""

            episodes.append(episode)

        podcast_metadata["title"] = root.findtext("channel/title")
        podcast_metadata["summary"] = root.findtext("channel/description")
        podcast_metadata["subtitle"] = root.findtext(
            "channel/itunes:subtitle",
            namespaces={"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"},
        )
        podcast_metadata["authorName"] = root.findtext(
            "channel/itunes:author",
            namespaces={"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"},
        )
        podcast_metadata["imageUrl"] = root.findtext("channel/image/url")
        podcast_metadata["rssOwnerName"] = root.findtext(
            "channel/itunes:owner/itunes:name",
            namespaces={"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"},
        )
        podcast_metadata["rssOwnerPublicEmail"] = root.findtext(
            "channel/itunes:owner/itunes:email",
            namespaces={"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"},
        )
        podcast_metadata["websiteUrl"] = root.findtext("channel/link")
        podcast_metadata["isExplicitContent"] = root.findtext(
            "channel/itunes:explicit",
            namespaces={"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"},
        )
        podcast_metadata["copyright"] = root.findtext("channel/copyright")
        podcast_metadata["language"] = root.findtext("channel/language")
        podcast_metadata["contentType"] = root.findtext(
            "channel/itunes:type",
            namespaces={"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"},
        )
        podcast_metadata["genres"] = [
            category.get("text")
            for category in root.findall(
                ".//itunes:category",
                namespaces={"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"},
            )
        ]

        return {"podcast_metadata": podcast_metadata, "episodes": episodes}


class PodcastDataSaver:
    def __init__(self, data):
        self.data = data

    def save(self):
        podcast_metadata = self.data.get("podcast_metadata")
        episodes = self.data.get("episodes")

        with transaction.atomic():
            podcast, created = Podcast.objects.get_or_create(
                title=podcast_metadata["title"]
            )
            self.update_podcast_metadata(podcast, podcast_metadata)
            self.save_episodes(podcast, episodes)

    def update_podcast_metadata(self, podcast, metadata):
        podcast.summary = metadata["summary"]
        podcast.subtitle = metadata["subtitle"]
        podcast.authorName = metadata["authorName"]
        podcast.imageUrl = metadata["imageUrl"]
        podcast.rssOwnerName = metadata["rssOwnerName"]
        podcast.rssOwnerPublicEmail = metadata["rssOwnerPublicEmail"]
        podcast.websiteUrl = metadata["websiteUrl"]
        podcast.isExplicitContent = metadata["isExplicitContent"]
        podcast.copyright = metadata["copyright"]
        podcast.language = metadata["language"]
        podcast.contentType = metadata["contentType"]
        podcast.genres = metadata["genres"]
        podcast.save()

    def save_episodes(self, podcast, episodes):
        for episode_data in episodes:
            if not PodcastEpisode.objects.filter(
                podcast=podcast, audioUrl=episode_data["audioUrl"]
            ).exists():
                episode = PodcastEpisode(
                    podcast=podcast,
                    title=episode_data["title"],
                    duration=episode_data["duration"],
                    audioUrl=episode_data["audioUrl"],
                    publish_date=episode_data["publish_date"],
                    explicit=episode_data["explicit"] == "yes",
                    imageUrl=episode_data.get("imageUrl", ""),
                    summary=episode_data["summary"],
                    description=episode_data["description"],
                )
                episode.save()


def main(rss_url):
    parser = PodcastParser(rss_url)
    data = parser.parse()
    if data:
        saver = PodcastDataSaver(data)
        saver.save()
