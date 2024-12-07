Web Content Scraper

Extract text content from webpages
Download PDF files from websites
Recursively explore and scrape linked pages within the same domain

Features

Webpage Text Extraction: Saves webpage content as clean text files
PDF Download: Automatically downloads PDF files found on the page
Recursive Scraping: Explores and scrapes linked pages within the same website
Filename Sanitization: Creates safe, timestamp-based filenames
Directory Management: Automatically creates output directory if it doesn't exist

Prerequisites
Required Libraries

os
requests
beautifulsoup4
datetime

Installation
bash

pip install requests beautifulsoup4
Usage
Scraping a Website
python

# Basic usage
url = 'https://example.com'
scrape_website(url, directory="./output")

Functions
download_pdf(url, directory=".")

Downloads all PDF files from a given webpage
Saves PDFs in the specified directory

save_webpage_content(url, directory=".")

Extracts text content from a webpage
Saves content as a text file with timestamp
Removes HTML tags and empty lines

scrape_website(url, directory=".")

Main function for recursive website scraping
Saves webpage content and downloads PDFs
Explores links within the same domain
