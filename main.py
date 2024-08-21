from bs4 import BeautifulSoup
import pandas
import numpy
import os
from typing import Dict, List, Union

# for each file
# - get file into soup
# - extract meaningful data from soup: Title, Summary, Characters (POV, Appearing, Referenced), Creatures, Chapter Rating (rating, votes)
# - load and append meaningful data into pandas DF

FILE_DIR = './chapter-data/101/' # looking at book 1 only

class AsoiafAnalyser():
    def __init__(self):
        self.chapter_files = [f for f in os.listdir(FILE_DIR) if '.html' in f]
        self.df = pandas.DataFrame(columns=["title","synposys","summary","characters.pov","characters.appearing","characters.referenced","rating"])

    def extract_from_html(self):
        for file_name in self.chapter_files:
            index = file_name.split('.')[0]
            path = FILE_DIR + file_name
            with open(path, 'r', encoding='utf-8') as file: html_content = file.read()
            soup_content = BeautifulSoup(html_content, 'html.parser')
            
            title = soup_content.find('h1').get_text()
            synposys = soup_content.find(class_='subhead').get_text()
            
            rating = self.HTMLExtract.get_chapter_rating(soup_content)
            summary = self.HTMLExtract.get_summary(soup_content)
            characters = self.HTMLExtract.get_characters(soup_content)

            entry = {
                'title': title, 
                'synposys': synposys, 
                'rating': rating, 
                'summary': summary,
                'characters.pov': characters['pov'],
                'characters.appearing': characters['appearing'],
                'characters.referenced': characters['referenced']
            }
            self.df = pandas.concat([self.df, pandas.DataFrame([entry], index=[index])])

            self.HTMLExtract.get_characters(soup_content)


    class HTMLExtract(): 
        @staticmethod
        def get_chapter_rating(soup_content: BeautifulSoup) -> float:
            r_heading = soup_content.find('h2', id='rating')
            if r_heading:
                r_content = r_heading.find_next_sibling('p')
                if r_content and 'Rating:' in r_content.text:
                    rating_str = r_content.get_text().split(":")[1]
                    rating = float(rating_str.strip(" "))
                    return rating
            return 0
        
        @staticmethod
        def get_summary(soup_content: BeautifulSoup) -> str:
            # the summary content is between the h2 headings: 'summary' and 'notes-characters'

            start_tag = soup_content.find('h2', id="summary")
            end_tag = soup_content.find('h2',id="notes-characters")
            paragraphs = []

            for element in start_tag.find_next_siblings():
                if element == end_tag: break
                paragraphs.append(element.get_text())
            
            summary_text = '\n'.join(paragraphs)

            return summary_text


        @staticmethod
        def get_characters(soup_content: BeautifulSoup) -> Dict[str, Union[str, List[str]]]:
            # expected structure:
            # <h2, id="notes-characters">: characters
            # <h3>POV<\h3> {content}, <h3>appearing<\h3> {content}, <h3>referenced<\h3> {content}
            # <h2, id unknown>

            characters = {'pov':"", 'appearing':[], 'referenced':[]}
            start_tag = soup_content.find('h2',id="notes-characters")

            for element in start_tag.find_next_siblings():
                if element.get_text() == "POV":
                    # POV character name is the text preceeding first comma
                    pov_el = element.find_next_sibling()
                    temp_text = pov_el.get_text()
                    pov_character = temp_text.split(",")[0]
                    characters['pov'] = pov_character
                
                elif element.get_text() == "Appearing":
                    # comma seperated list of characters are on first bullet point only
                    appearing_el = element.find_next_sibling()
                    html_el = appearing_el.find_next('li') 
                    appearing_characters = [a.get_text() for a in html_el.find_all('a')]
                    characters['appearing'] = appearing_characters

                elif element.get_text() =="Referenced":
                    # each <li> contains the character name
                    referenced_el = element.find_next_sibling()
                    li_elements = referenced_el.find_all('li')
                    referenced_characters = [li.find('a').get_text() for li in li_elements]
                    characters['referenced'] = referenced_characters
            
            return characters

if __name__ == "__main__":
    analyzer = AsoiafAnalyser()
    analyzer.extract_from_html()
    print(analyzer.df)

    # analyzer.HTMLExtract.get_characters()