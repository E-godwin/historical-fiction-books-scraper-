# Import Libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Base category URL for Historical Fiction
base_url = "https://books.toscrape.com/catalogue/category/books/historical-fiction_4/"
page_url = "index.html"  # Initial page
books = []  # List to store book data

# Keep scraping until we get 400 books or run out of pages
while len(books) <= 400:
    # Construct full URL for the current page
    full_url = base_url + page_url
    response = requests.get(full_url)

    # Stop if the page doesn't load properly
    if response.status_code != 200:
        print("Page not found:", full_url)
        break

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all book entries on the page
    book_list = soup.find_all('article', class_='product_pod')

    # Loop through each book on the page
    for book in book_list:
        # Extract book title
        title = book.h3.a['title']

        # Extract and clean price (remove £ or any weird symbols)
        price = book.find('p', class_='price_color').text.strip().lstrip('Â££')

        # Extract availability text (e.g., "In stock")
        availability = book.find('p', class_='instock availability').text.strip()

        # Extract the star rating (e.g., "Three", "Five")
        rating = book.p['class'][1]

        # Extract the product page link and convert it to a full URL
        relative_url = book.h3.a['href'].replace('../../../', '')
        product_url = f"https://books.toscrape.com/catalogue/{relative_url}"

        # Add the scraped data to our list
        books.append({
            'Title': title,
            'Price (£)': float(price),
            'Availability': availability,
            'Rating': rating,
            'Product URL': product_url
        })

        # Stop if we’ve reached our 400 book limit
        if len(books) >= 400:
            break

    # Find the "Next" button to go to the next page
    next_button = soup.find('li', class_='next')
    if next_button:
        page_url = next_button.a['href']  # e.g., 'page-2.html'
        time.sleep(1)  # Pause to avoid overwhelming the server
    else:
        # No more pages left
        break

# Convert the list of books to a DataFrame
df = pd.DataFrame(books)

# Save the scraped data to a CSV file
filename = 'historical_fiction_books.csv'
df.to_csv(filename, index=False)

