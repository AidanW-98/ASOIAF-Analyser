import json
import pandas as pd
import sqlite3

# where we apply transformations
class AsoiafAnalyzer():
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

        self.df['characters_appearing'] = self.df['characters_appearing'].apply(json.dumps)
        self.df['characters_referenced'] = self.df['characters_appearing'].apply(json.dumps)

        self.connection = sqlite3.connect(':memory:')
        self.df.to_sql('dataframe', self.connection)
    
    def query(self, sql_query: str):
        result = pd.read_sql_query(sql_query, self.connection)
        print(result)

    def example_quries(self):
        print("What's the best chapter where Daenerys Targaryen appears?")
        sql_query = "SELECT title FROM dataframe WHERE characters_appearing LIKE '%Daenerys Targaryen%' ORDER BY rating DESC LIMIT 1"
        print(sql_query)
        self.query(sql_query)