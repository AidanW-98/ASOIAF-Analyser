from AsoiafDataProcessor import AsoiafDataProcessor

# for each file
# - get file into soup
# - extract meaningful data from soup: Title, Summary, Characters (POV, Appearing, Referenced), Creatures, Chapter Rating (rating)
# - load and append meaningful data into pandas DF
# - transform with pandas queries (SQL-like)

if __name__ == "__main__":
    analyzer = AsoiafDataProcessor()
    analyzer.process_chapters()
    df = analyzer.df
    print(df)