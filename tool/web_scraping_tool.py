import logging
import requests
from bs4 import BeautifulSoup
from langchain.tools import tool

def truncate_base64(content):
    """Truncate base64-encoded data to only keep till 'jpeg'."""
    if "base64" in content:
        parts = content.split("base64,")
        return parts[0] if len(parts) > 1 else content
    return content

@tool("scrape_link", return_direct=True)
def scrape_link(url: str) -> str:
    """
    Scrapes a webpage and returns formatted text, image URLs, table HTML, and links in sequence.

    Parameters:
    - url (str): URL of the webpage to scrape.

    Returns:
    - str: A string summary of the page's content (text, image URLs, links, tables).
    """

    try:
        logging.info(f"Fetching webpage content from {url}")
        response = requests.get(url, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')

        content_list = []
        for element in soup.body.descendants:
            if element.name == 'p':
                content = element.get_text(strip=True)
                if content:
                    content_list.append({'type': 'text', 'content': truncate_base64(content)})

            elif element.name == 'img':
                img_src = element.get('src')
                if img_src:
                    full_url = requests.compat.urljoin(url, img_src)
                    content_list.append({'type': 'image', 'content': truncate_base64(full_url)})

            elif element.name == 'table':
                table_html = str(element)
                content_list.append({'type': 'table', 'content': truncate_base64(table_html)})

            elif element.name == 'a':
                link_href = element.get('href')
                link_text = element.get_text(strip=True)
                if link_href:
                    full_url = requests.compat.urljoin(url, link_href)
                    content_list.append({
                        'type': 'link',
                        'content': {
                            'url': truncate_base64(full_url),
                            'text': truncate_base64(link_text)
                        }
                    })

        text = ""
        for item in content_list:
            if item['type'] == 'text':
                text += f"Text: {item['content']}\n"
            elif item['type'] == 'image':
                text += f"Image URL: {item['content']}\n"
            elif item['type'] == 'table':
                text += f"Table HTML: {item['content']}\n"
            elif item['type'] == 'link':
                link = item['content']
                text += f"Link: {link['url']} (Text: {link['text']})\n"

        logging.info(f"Web scraping completed from {url}")
        return text

    except Exception as e:
        logging.error(f"Error scraping {url}: {e}")
        return "Failed to scrape the webpage."