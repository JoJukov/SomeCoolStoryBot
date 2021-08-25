import requests

NO_STYLE = 1

class BalabobaGenerateException(Exception):

    def __init__(self, message) -> None:
        super().__init__(f'Failed to get generated text: {message}')

class Style:
    '''
    Style option for `Balaboba.generate` method.

    Attributes:
    -----------------
    `description` : `str`
        Field contains name of style
    '''

    def __init__(self, description, id):
        self._id = id
        self.description = description

class Balaboba:
    '''
    Methods
    ------------
    `generate(query, style = NO_STYLE) -> str`
       Call *Balaboba* to generate text based on `query` and `style` parameters
    `getStyles() -> [Style]`
       Fetching styles
    '''

    API_URL   = "https://yandex.ru/lab/api/yalm"
    STYLE_URL = "/intros"
    QUERY_URL = "/text3"

    def getStyles(self):
        '''
        Fetching styles

        Returns
        ---------------
        The list of `Style` objects

        Throws
        ---------------
        `BalabobaFetchStylesException`
            When face an error getting or parsing response
        '''
        return 

    def __init__(self) -> None:
        pass

    def generate(self, query, style = NO_STYLE):
        '''
        Abusing *Balaboba* to generate text.

        Parameters
        ---------------
        `query` : `str`
            Initial text
        `style` : `Style`
            Style acuired from ~getStyles~ method

        Returns
        ----------------
        Generated text

        Throws
        ----------------
        `BalabobaGenerateException`
            When face an error getting or parsing response
        '''

        response = requests.post(
            self._queryUrl(),
            json=self._createQueryJsonRequest(query, style),
        ).json()
        return self._jsonResponseToText(response)

    def _createQueryJsonRequest(self, query, style):
        return {
            "query": query,
            "intro": style,
            "filter": 0,
        }

    def _jsonResponseToText(self, response):
        return response["query"] + response["text"]

    def _methodUrl(self, method):
        return f'{self.API_URL}/{method}'

    def _styleUrl(self):
        return self._methodUrl(self.STYLE_URL)
    
    def _queryUrl(self):
        return self._methodUrl(self.API_URL)
