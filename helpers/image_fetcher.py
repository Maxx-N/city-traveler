from io import BytesIO

import requests
from PIL import Image

from constants import openai


def fetch_wikipedia_image_url(subject: str) -> str | None:
    """Fetches the first image URL from the Wikipedia page of the given subject."""
    normalized_subject = subject.lower().strip().replace(" ", "_").replace("-", "_")
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{normalized_subject}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None
    image = response.json().get("originalimage")
    return image["source"] if image else None


def fetch_image_from_url(url: str) -> Image.Image | None:
    headers = {"User-Agent": "city-traveler/1.0"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"Error fetching image from URL {url}: {e}")
        return None


def fetch_wikipedia_image(subject: str):
    image_url = fetch_wikipedia_image_url(subject)
    if not image_url:
        return None
    return fetch_image_from_url(image_url)
