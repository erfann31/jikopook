import requests
from bs4 import BeautifulSoup


def extract_links_and_texts(link):
    response = requests.get(link)
    if response.status_code != 200:
        print(f"Failed to retrieve the content from {link}. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    texts_and_links = {}

    for tag in soup.find_all('a'):
        href = tag.get('href')
        text = tag.get_text(strip=True)
        if href and text:
            if not href.startswith('http'):
                href = link.rstrip('/') + href
            texts_and_links[text] = href

    return texts_and_links
