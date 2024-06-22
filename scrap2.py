import requests
from bs4 import BeautifulSoup
import os

CACHE_DIR = 'cache'

def ensure_cache_dir():
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

def get_cache_filename(page_number):
    return os.path.join(CACHE_DIR, f'page_{page_number}.html')

def is_page_cached(page_number):
    return os.path.exists(get_cache_filename(page_number))

def save_page_to_cache(page_number, content):
    with open(get_cache_filename(page_number), 'w', encoding='utf-8') as f:
        f.write(content)

def load_page_from_cache(page_number):
    with open(get_cache_filename(page_number), 'r', encoding='utf-8') as f:
        return f.read()

def scrape_titles_from_page(page_number):
    if is_page_cached(page_number):
        print(f'Loading page {page_number} from cache...')
        html_content = load_page_from_cache(page_number)
    else:
        url = f'https://www.wix.com/website/templates/html/all/{page_number}'
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            save_page_to_cache(page_number, html_content)
        else:
            print(f"Failed to retrieve page {page_number}. Status code: {response.status_code}")
            return []

    soup = BeautifulSoup(html_content, 'html.parser')
    titles = soup.find_all('div', class_='Q37wn8')
    if not titles:
        return []

    return [title.get_text().strip() for title in titles]

def scrape_all_titles(max_pages=50):
    ensure_cache_dir()
    all_titles = []
    page_number = 1

    while page_number <= max_pages:
        titles = scrape_titles_from_page(page_number)
        if not titles:
            break
        all_titles.extend(titles)
        page_number += 1
    
    return all_titles

if __name__ == '__main__':
    titles = scrape_all_titles(max_pages=50)
    for title in titles:
        print(title)
