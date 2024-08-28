from AsoiafDataProcessor import AsoiafDataProcessor
from AsoiafAnalyzer import AsoiafAnalyzer
from PromptToSQL import PromptToSQL

if __name__ == "__main__":
    # getting objects for example use case

    processor = AsoiafDataProcessor()
    ex_soup = AsoiafDataProcessor.load_html_as_soup("./chapter-data/101/006.html")
    processor.process_chapters()
    df = processor.df

    analyzer = AsoiafAnalyzer(processor.df)
    analyzer.sql_generator = PromptToSQL()

def run_demo(analyzer: AsoiafAnalyzer):
    nl_query = input("What would you like to know about ASOIAF?\t")
    query = analyzer.get_query_by_natural_language(nl_query)
    analyzer.query(query)