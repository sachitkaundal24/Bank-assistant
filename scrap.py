import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime
import re

def download_pdf(url, directory="."):
    # Send the get request for URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        print("Scraping content from:", url)

        # Find all anchor tags that have href attribute ending with pdf
        pdf_links = soup.find_all('a', href=lambda href: href and href.endswith('.pdf'))
        print("Found PDF links:", pdf_links)

        # Download PDFs
        for link in pdf_links:
            pdf_url = urljoin(url, link['href'])
            # Construct file path inside the directory
            filename = os.path.join(directory, os.path.basename(pdf_url))
            with open(filename, 'wb') as f:
                f.write(requests.get(pdf_url).content)
            print(f"Downloaded: {filename}")
    else:
        print("Failed to retrieve webpage:", response.status_code)

def save_webpage_content(url, directory="."):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.title.string.strip() if soup.title else "Untitled"

        # Sanitize title to remove invalid characters for filenames
        sanitized_title = re.sub(r'[<>:"/\\|?*]', '_', title)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        # Save the content in the provided directory (make sure to add folder path)
        filename = os.path.join(directory, f"{sanitized_title}_{timestamp}_webpage_content.txt")

        # Save webpage content without HTML tags
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(line for line in soup.get_text().splitlines() if line.strip()))
        print(f"Saved webpage content: {filename}")
    else:
        print("Failed to retrieve webpage:", response.status_code)

def scrape_website(url, directory="."):
    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

    visited_urls = {}

    def scrape_url_recursive(url):
        if url in visited_urls:
            return
        visited_urls[url] = True

        # Save webpage content in the given directory
        save_webpage_content(url, directory)

        # Download PDFs in the given directory
        download_pdf(url, directory)

        # Send a get request to the URL
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            # Find all anchor tags and recursively scrape their URLs
            links = soup.find_all('a', href=True)
            for link in links:
                next_url = urljoin(url, link['href'])
                if urlparse(next_url).netloc == urlparse(url).netloc:
                    scrape_url_recursive(next_url)
        else:
            print(f"Failed to retrieve {url}: {response.status_code}")

    scrape_url_recursive(url)

# Call the scraping function with a specific directory
url = 'https://medium.com/@prajwalkankate/what-is-genai-7e10f008e749'
scrape_website(url, directory="C:/Users/sachit.kaundal/Desktop/Graq/content/tsb")  # Specify your `tsb` folder

