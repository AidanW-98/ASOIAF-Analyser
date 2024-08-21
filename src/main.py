from AsoiafDataProcessor import AsoiafDataProcessor
from AsoiafAnalyzer import AsoiafAnalyzer

# for each file
# - get file into soup
# - extract meaningful data from soup: Title, Summary, Characters (POV, Appearing, Referenced), Creatures, Chapter Rating (rating)
# - load and append meaningful data into pandas DF
# - transform with pandas queries (SQL-like)

if __name__ == "__main__":
    processor = AsoiafDataProcessor()
    processor.process_chapters()
    df = processor.df
    print(df)

    analyzer = AsoiafAnalyzer(df)
    analyzer.example_quries()