import requests
from bs4 import BeautifulSoup

def scrape_titles_from_page(page_number):
    # URL of the website with the current page number
    url = f'https://www.wix.com/website/templates/html/all/{page_number}'

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all template titles (assuming they are within <div> tags with a specific class)
        titles = soup.find_all('div', class_='Q37wn8')
        
        # If no titles are found, return an empty list to stop the loop
        if not titles:
            return []

        # Extract and return the text from each title
        return [title.get_text().strip() for title in titles]
    else:
        print(f"Failed to retrieve page {page_number}. Status code: {response.status_code}")
        return []

def scrape_all_titles(max_pages=50):
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
    # Scrape titles from the first 50 pages (or until no more pages are found)
    titles = scrape_all_titles(max_pages=50)
    
    # Print all the titles
    for title in titles:
        print(title)
