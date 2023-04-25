from json import loads
import pandas as pd
from os import path
import duckdb

class CovidReportData:
    """Generic class for querying covid data that can be used for downstream reports"""

    def __init__(self, dataPath: str, description: str, query: str):
        if not isinstance(dataPath, str):
            raise TypeError('Error: dataPath must be of type <str>')
        if not isinstance(description, str):
            raise TypeError('Error: description must be of type <str>')
        if not isinstance(query, str):
            raise TypeError('Error: query must be of type <str>')

        self.dataPath: str = dataPath
        self.description: str = description
        self.query: str = query

        if not path.exists(self.dataPath):
            raise FileNotFoundError('Error: dataset not loaded. Please run \'python dataset.py load\' to retrieve dataset.')

        self.data = loads(open(self.dataPath, 'r').read())
    
    def query_data(self) -> pd.DataFrame :
        """Queries self.data as a df using self.query and returns a df result
        
        Returns:
            result (pd.DataFrame): the resulting df from the query"""
        print('')
        print(f'Retrieving {self.description}')
        print('')

        df = pd.DataFrame(self.data)
        
        return duckdb.sql(self.query).df()
