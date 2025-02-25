from operator import truediv

from bs4 import BeautifulSoup
import csv


def scrape_reviews():
    scraping = True
    count = 1
    review_list = []
    while scraping:
        try:
            file_path = f"ck_scrapes/html{count}.txt"
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            soup = BeautifulSoup(content, "html.parser")
            narrowed_file = soup.find('div', class_='center pa3')
            soup = BeautifulSoup(str(narrowed_file), "html.parser")
            reviews = soup.find_all("p", class_="f4 lh-copy ma0")
            reviews = [review.text for review in reviews]
            review_list.append(reviews)
            count += 1
        except FileNotFoundError:
            scraping = False

    output_file = "ck_reviews/scraped_reviews.csv"
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Review"])  # Header
        for review in review_list:
            writer.writerow([review])
scrape_reviews()