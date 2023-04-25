from os import path, remove, listdir, makedirs
from requests import get, Response
from json import loads, dumps
from typing import List

class API:
    """Static class to retrieve data from api endpoints"""

    ASSETS_DIR_NAME: str = 'assets'

    JSON_DIR_NAME: str = 'json'
    JSON_DIR: str = path.join(ASSETS_DIR_NAME, JSON_DIR_NAME)

    COVID_DATASET_FILENAME: str = 'coviddata.json'
    COVID_DATASET_FILEPATH: str = path.join(JSON_DIR, COVID_DATASET_FILENAME)

    DEFAULT_ROW_LIMIT: int = 50_000
    
    @staticmethod
    def get_as_list(url: str) -> str :
        """Retrieves data from api as a list
        
        Args:
            url (str): the absolute api endpoint path
        
        Returns:
            contents (dict): the contents of the api endpoint as a dict object
        """
        if not isinstance(url, str):
            raise TypeError('Error: url must be of type <str>')
        
        contents: List[dict] = []
        payloadCount: int = 0
        payloadComplete: bool = False
    
        while not payloadComplete:
            offset: int = payloadCount * API.DEFAULT_ROW_LIMIT
            chunkedUrl: str = '{}?$limit={}'.format(
                url,
                API.DEFAULT_ROW_LIMIT
            )

            if offset:
                chunkedUrl += '&$offset={}'.format(offset)

            response: Response = get(chunkedUrl)

            if response.ok:
                data: list = response.json()
                contents.extend(data)
                payloadCount += 1

                if len(data) != API.DEFAULT_ROW_LIMIT:
                    payloadComplete = True
                    break
            else:
                ['[ERROR] dataset load failed:']
                raise ConnectionError(response.reason)

        makedirs(API.JSON_DIR, exist_ok = True)
        open(API.COVID_DATASET_FILEPATH, 'w').write(dumps(contents))

        print('[SUCCESS] dataset successfully loaded.')


    @staticmethod
    def clear_json_data():
        """Deletes all .json files in the 'assets/json' directory
        """
        for filename in listdir(API.JSON_DIR):
            filePath: str = path.join(API.JSON_DIR, filename)
            remove(filePath)