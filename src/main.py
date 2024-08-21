from AsoiafDataProcessor import AsoiafDataProcessor
from AsoiafAnalyzer import AsoiafAnalyzer
from PromptToSQL import PromptToSQL

if __name__ == "__main__":
    processor = AsoiafDataProcessor()
    processor.process_chapters()
    df = processor.df
    print(df)

    analyzer = AsoiafAnalyzer(df)
    analyzer.example_quries()

    nl_query = input("What would you like to know about ASOIAF Chapters?")
    sql_query = analyzer.get_query_by_natural_language(nl_query)
    analyzer.query(sql_query)