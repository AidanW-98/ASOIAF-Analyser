from bs4 import BeautifulSoup
import pandas
import os
from typing import Dict, List, Union

FILE_DIR = './chapter-data/101/' # looking at book 1 only

class AsoiafDataProcessor():
    def __init__(self):
        self.chapter_files = [f for f in os.listdir(FILE_DIR) if '.html' in f]
        self.df = pandas.DataFrame(columns=["title","synposys","summary","characters_pov","characters_appearing","characters_referenced","rating"])

    @staticmethod
    def load_html_as_soup(html_file_path) -> BeautifulSoup:
            with open(html_file_path, 'r', encoding='utf-8') as file: 
                html_content = file.read()
            soup_content = BeautifulSoup(html_content, 'html.parser')
            return soup_content
    
    def process_chapters(self):
        for file_name in self.chapter_files:
            index = file_name.split('.')[0]
            path = FILE_DIR + file_name
            soup_content = AsoiafDataProcessor.load_html_as_soup(path)

            title = soup_content.find('h1').get_text()
            synposys = soup_content.find(class_='subhead').get_text()
            rating = self.SoupExtract.get_chapter_rating(soup_content)
            summary = self.SoupExtract.get_summary(soup_content)
            characters = self.SoupExtract.get_characters(soup_content)

            entry = {
                'title': title, 
                'synposys': synposys, 
                'rating': rating, 
                'summary': summary,
                'characters_pov': characters['pov'],
                'characters_appearing': characters['appearing'],
                'characters_referenced': characters['referenced']
            }

            self.df = pandas.concat([self.df, pandas.DataFrame([entry], index=[index])])

    class SoupExtract(): 
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