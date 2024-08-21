import json
import pandas as pd
import sqlite3
from PromptToSQL import PromptToSQL

# where we apply transformations
class AsoiafAnalyzer():
    sql_generator = None
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
    
    def get_query_by_natural_language(self, nl_query: str) -> str:
        if self.sql_generator is None:
            self.sql_generator = PromptToSQL()
        sql_query = self.sql_generator.get_sql(nl_query)

        print("Based on user query, the following SQL has been produced:\n", sql_query, "\nresult:")
        return sql_query