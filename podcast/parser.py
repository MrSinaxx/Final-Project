import xml.etree.ElementTree as ET
import json
import requests
from django.db import transaction
from .models import Podcast, PodcastEpisode


def parse_rss_feed(rss_url):
    try:
        response = requests.get(rss_url)
        response.raise_for_status()
        xml_data = response.text

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
            category.text
            for category in root.findall(
                "channel/itunes:category/itunes:category",
                namespaces={"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"},
            )
        ]

        return {"podcast_metadata": podcast_metadata, "episodes": episodes}

    except requests.exceptions.RequestException as e:
        print(f"Error fetching RSS feed: {e}")
        return None


def save_podcast_data_to_db(data):
    podcast_metadata = data.get("podcast_metadata")
    episodes = data.get("episodes")

    with transaction.atomic():
        podcast, created = Podcast.objects.get_or_create(
            title=podcast_metadata["title"]
        )

        podcast.summary = podcast_metadata["summary"]
        podcast.subtitle = podcast_metadata["subtitle"]
        podcast.authorName = podcast_metadata["authorName"]
        podcast.imageUrl = podcast_metadata["imageUrl"]
        podcast.rssOwnerName = podcast_metadata["rssOwnerName"]
        podcast.rssOwnerPublicEmail = podcast_metadata["rssOwnerPublicEmail"]
        podcast.websiteUrl = podcast_metadata["websiteUrl"]
        podcast.isExplicitContent = podcast_metadata["isExplicitContent"]
        podcast.copyright = podcast_metadata["copyright"]
        podcast.language = podcast_metadata["language"]
        podcast.contentType = podcast_metadata["contentType"]
        podcast.genres = ", ".join(podcast_metadata["genres"])

        podcast.save()

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
