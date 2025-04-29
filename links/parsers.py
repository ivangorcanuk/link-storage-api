import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .models import LinkType


def parse_link_metadata(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        def get_og_property(prop):
            meta = soup.find('meta', property=f'og:{prop}')
            return meta['content'] if meta else None

        title = get_og_property('title') or soup.title.string if soup.title else url
        description = get_og_property('description') or soup.find('meta', attrs={'name': 'description'})[
            'content'] if soup.find('meta', attrs={'name': 'description'}) else None
        image_url = urljoin(url, get_og_property('image')) if get_og_property('image') else None

        link_type = detect_link_type(soup) or LinkType.WEBSITE.value

        return {
            'title': title[:255] if title else None,
            'description': description,
            'image_url': image_url,
            'link_type': link_type
        }
    except Exception as e:
        return {
            'title': url,
            'link_type': LinkType.WEBSITE.value
        }


def detect_link_type(soup):
    if soup.find('meta', property='og:type'):
        og_type = soup.find('meta', property='og:type')['content'].lower()
        if 'book' in og_type:
            return LinkType.BOOK.value
        elif 'article' in og_type:
            return LinkType.ARTICLE.value
        elif 'video' in og_type:
            return LinkType.VIDEO.value
        elif 'music' in og_type:
            return LinkType.MUSIC.value
    return None