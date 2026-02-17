# web_scraper.py
import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "http://books.toscrape.com/catalogue/category/books_1/index.html"

def scrape_books(url):
    books = []
    while url:
        res = requests.get(url)
        if res.status_code != 200:
            print("Failed to fetch page")
            break
        soup = BeautifulSoup(res.text, "html.parser")
        for book in soup.select(".product_pod"):
            title = book.h3.a["title"]
            price = book.select(".price_color")[0].text
            availability = book.select(".availability")[0].text.strip()
            books.append({"Title": title, "Price": price, "Availability": availability})

        next_btn = soup.select(".next a")
        if next_btn:
            next_page = next_btn[0]["href"]
            url = "/".join(url.split("/")[:-1]) + "/" + next_page
        else:
            url = None
    return books

if __name__ == "__main__":
    print("Scraping books...")
    data = scrape_books(URL)
    df = pd.DataFrame(data)
    df.to_csv("books.csv", index=False)
    print(f"Saved {len(data)} books to books.csv")
