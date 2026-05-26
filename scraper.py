"""
Web Scraper for books.toscrape.com
Extracts book titles and prices, saves to CSV.
Author: [Sudheera uthpala]
Date: May 2026
"""

import requests
from bs4 import BeautifulSoup
import csv
import time

# Target website (a safe, practice-friendly site)
URL = "http://books.toscrape.com/"

print(f"🌐 Fetching {URL} ...")
response = requests.get(URL)
response.encoding = 'utf-8'  # Force correct encoding

# Check if download worked (status code 200 = OK)
if response.status_code != 200:
    print(f"❌ Failed to get page. Status code: {response.status_code}")
    exit()
else:
    print("✅ Page downloaded successfully!")

# Create a BeautifulSoup object to read the HTML
soup = BeautifulSoup(response.text, "html.parser")
print("🔍 Parsing HTML...")

# Each book is inside an <article> tag with class "product_pod"
books = soup.find_all("article", class_="product_pod")
print(f"📚 Found {len(books)} books on this page.")

# This will hold all the scraped data as [title, price] pairs
scraped_data = []

for index, book in enumerate(books, start=1):
    # Extract title (inside <h3> -> <a> -> title attribute)
    title_tag = book.find("h3").find("a")
    title = title_tag.get("title")  # gets the full book name
    
    # Extract price (inside <p class="price_color">)
    price_tag = book.find("p", class_="price_color")
    price = price_tag.text  # gets text like "£51.77"
    
    # Add to our list
    scraped_data.append([title, price])
    
    # Show progress (good for debugging)
    print(f"   [{index}] {title} - {price}")
    
    # Be polite: wait 0.2 seconds before next request (not strictly needed for one page, but good habit)
    time.sleep(0.2)

# Define output filename
CSV_FILENAME = "books.csv"

with open(CSV_FILENAME, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    # Write header row
    writer.writerow(["Title", "Price"])
    # Write all book rows
    writer.writerows(scraped_data)

print(f"💾 Data saved to {CSV_FILENAME}")
print(f"📊 Total books saved: {len(scraped_data)}")

print("\n🎉 Scraping completed successfully!")
print("Open books.csv with Excel or any text editor to see the results.")