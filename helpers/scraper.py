import requests
from bs4 import BeautifulSoup


def fetch_website_contents(url: str) -> str | None:
    """Fetches the contents of a website given its URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string if soup.title else "No title found"
    if soup.body:
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
    else:
        text = ""
    return title + "\n\n" + text


def fetch_wikipedia_page(subject: str) -> str | None:
    url = f"https://en.wikipedia.org/wiki/{subject.lower().strip().replace(' ', '_').replace('-', '_')}"
    return fetch_website_contents(url)
