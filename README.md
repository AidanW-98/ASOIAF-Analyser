# ASOIAF Analyser

This simple project aims to analyse ASOIAF Chapters based on data from [Tower Of The Hand](https://towerofthehand.com/) (aka TOTH). It does so by scraping the website content, structuring & cleaning the data, producing analysis summaries, and providing a LLM-based assistant.

## Tech Summary

This Python project is a very small scale local Data Engineering project - as such data will only exist on the local machine. Cloud services will not be used.

Data will go through an ELT pipeline by the following means:

### Extract (ingest)

Web scrapers via `requests` and `BeautifulSoup` will be called on `towerofthehand.com` and the data would be stored in a raw format of HTML content.

This will be done by the chapter; TOTH follows the format of: `towerofthehand.com/books/<book_ID>/<chapter_ID>`. `book_ID` is 101 for GoT and the `chapter_ID` iterates from `001` onwards for each chapter.

### Load

Once we have the data as HTML content, this will be loaded into a *Pandas DataFrame*.

### Transform

The transformations will be done through Pandas Queries. Any required cleaning will be done here also.

### LLM Integration

The aim is to produce an LLM which could take in a natural language input, produce a Pandas query based on that, and display the output queried data.