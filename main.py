from bs4 import BeautifulSoup
import pandas
import numpy
import os

# for each file
# - get file into soup
# - extract meaningful data from soup: Title, Summary, Characters (POV, Appearing, Referenced), Creatures, Chapter Rating (rating, votes)
# - load and append meaningful data into pandas DF

FILE_DIR = './chapter-data/101/' # looking at book 1 only

class AsoiafAnalyser():
    def __init__(self):
        chapter_files = [f for f in os.listdir(FILE_DIR) if '.html' in f]
        df = pandas.DataFrame(columns=["title","blurb","rating"])

    def get_chapter_rating(self, soup_content: BeautifulSoup) -> float:
        r_heading = soup_content.find('h2', id='rating')
        if r_heading:
            r_content = r_heading.find_next_sibling('p')
            if r_content and 'Rating:' in r_content.text:
                rating_str = r_content.get_text().split(":")[1]
                rating = float(rating_str.strip(" "))
                return rating
        return 0

    def extract_from_html(self):
        for file_name in self.chapter_files:
            path = FILE_DIR + file_name
            with open(path, 'r', encoding='utf-8') as file: html_content = file.read()
            soup_content = BeautifulSoup(html_content, 'html.parser')
            
            index = int(file_name.split('.')[0])        # this doesn't work correctly
            title = soup_content.find('h1').get_text()
            synposys = soup_content.find(class_='subhead').get_text()
            rating = self.get_chapter_rating(soup_content)

            entry = {'index':index, 'title': title, 'blurb': synposys, 'rating': rating}
            self.df = pandas.concat([self.df, pandas.DataFrame([entry])])