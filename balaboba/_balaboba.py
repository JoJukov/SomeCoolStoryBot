import requests

DISCLAIMER = '''
Балабоба не принимает запросы на острые темы,
например, про политику или религию. Люди могут слишком серьёзно
отнестись к сгенерированным текстам.

Вероятность того, что запрос задаёт одну из острых тем, определяет
нейросеть, обученная на оценках случайных людей. Но она может
перестараться или, наоборот, что-то пропустить.
'''


class BalabobaRequestFailedException(Exception):
    def __init__(self, message) -> None:
        super().__init__(f'Failed to get generated text: {message}')


class BalabobaInvalidQueryException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(DISCLAIMER, *args)


class Style:
    '''
    Style option for `Balaboba.generate` method.

    Attributes:
    -----------------
    `name` : `str`
        Short description of style option
    `description` : `str`
        Long description of style option
    '''
    def __init__(self, _id, name, description):
        self._id = _id
        self.name = name
        self.description = description

    def __str__(self):
        return self.name


NO_STYLE = Style(0, '', '')


class Balaboba:
    '''
    Methods
    ------------
    `generate(query, style = NO_STYLE) -> str`
       Call *Balaboba* to generate text based on `query` and `style` parameters
    `getStyles() -> [Style]`
       Fetching styles
    '''

    API_URL = "https://yandex.ru/lab/api/yalm"
    STYLE_URL = "intros"
    QUERY_URL = "text3"

    def __init__(self) -> None:
        pass

    def getStyles(self):
        '''
        Fetching styles

        Returns
        ---------------
        The list of `Style` objects

        Throws
        ---------------
        `BalabobaRequestFailedException`
            When face an error getting or parsing response
        '''

        jsonResponse = self._checkedGet(
            [
                "intros",
            ],
            self._styleUrl(),
        )

        intros = jsonResponse["intros"]

        for intro in intros:
            if len(intro) < 3:
                raise BalabobaRequestFailedException(
                    "Some styles contas too few parameters")

        return self._processIntros(intros)

    def generate(self, query, style=NO_STYLE, filter=1):
        '''Abusing *Balaboba* to generate text.

        Parameters
        ---------------
        `query` : `str`
            Initial text
        `style` : `Style`, optional
            Style acuired from ~getStyles~ method
        `filter` : `int`, optional
            Some unknown parameter

        Returns
        ----------------
        Generated text

        Throws
        ----------------
        `BalabobaRequestFailedException`
            When face an error getting or parsing response
        `BalabobaInvalidQueryException`
            Read DISCLAIMER
        '''

        jsonResponse = self._checkedPost(
            [
                "query",
                "text",
            ],
            self._queryUrl(),
            json=self._createQueryJsonRequest(query, style, filter),
        )

        if jsonResponse["bad_query"] == 1:
            raise BalabobaInvalidQueryException()

        return self._jsonResponseToText(jsonResponse)

    def _checkedPost(self, *args, **kwargs):
        return self._checkedRequest("POST", *args, **kwargs)

    def _checkedGet(self, *args, **kwargs):
        return self._checkedRequest("GET", *args, **kwargs)

    def _checkedRequest(self, method, checkFields, url, *args, **kwargs):
        try:
            response = requests.request(url=url,
                                        method=method,
                                        *args,
                                        **kwargs)
        except:
            raise BalabobaRequestFailedException(
                f'Request to "{self._queryUrl()}" failed')

        try:
            jsonResponse = response.json()
        except:
            raise BalabobaRequestFailedException(
                f'Failed to parse to json: "{response.text}"')

        for field in checkFields:
            if jsonResponse.get(field) == None:
                raise BalabobaRequestFailedException(
                    f'No "{field}" value in response')

        if jsonResponse["error"] == 1:
            raise BalabobaRequestFailedException(
                "Balaboba failed to process request")

        return jsonResponse

    def _createQueryJsonRequest(self, query, style, filter):
        return {
            "query": query,
            "intro": style._id,
            "filter": filter,
        }

    def _jsonResponseToText(self, response):
        return response["query"] + response["text"]

    def _processIntros(self, intros):
        styles = []

        for intro in intros:
            style = Style(
                intro[0],
                intro[1],
                intro[2],
            )

            styles.append(style)

        return styles

    def _methodUrl(self, method):
        return f'{self.API_URL}/{method}'

    def _styleUrl(self):
        return self._methodUrl(self.STYLE_URL)

    def _queryUrl(self):
        return self._methodUrl(self.QUERY_URL)
