from bs4 import BeautifulSoup
import pandas
import numpy
import os


# for each file
# - get file into soup
# - extract meaningful data from soup: Title, Summary, Characters (POV, Appearing, Referenced), Creatures, Chapter Rating (rating, votes)
# - load and append meaningful data into pandas DF

FILE_DIR = './chapter-data/101/'
chapter_files = [f for f in os.listdir(FILE_DIR) if '.html' in f]

def get_chapter_rating(soup_content: BeautifulSoup) -> float:
    r_heading = soup_content.find('h2', id='rating')
    if r_heading:
        r_content = r_heading.find_next_sibling('p')
        if r_content and 'Rating:' in r_content.text:
            rating_str = r_content.get_text().split(":")[1]
            rating = float(rating_str.strip(" "))
            return rating
    return 0


df = pandas.DataFrame(columns=["title","blurb","rating"])
for file_name in chapter_files:
    path = FILE_DIR + file_name
    with open(path, 'r', encoding='utf-8') as file: html_content = file.read()
    soup_content = BeautifulSoup(html_content, 'html.parser')
    
    title = soup_content.find('h1').get_text()
    try: blurb = soup_content('.subhead')[0].get_text()
    except: blurb = ""
    rating = get_chapter_rating(soup_content)

    entry = {'title': title, 'blurb': blurb, 'rating': rating}
    df = pandas.concat([df, pandas.DataFrame([entry])])