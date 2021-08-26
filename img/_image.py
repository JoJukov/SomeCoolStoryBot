import requests
from typing import Final

URL: Final = "https://thispersondoesnotexist.com/image"


class ImageHttpRequestFailedException(Exception):
    def __init__(self):
        super().__init__(f"Error occurred while trying to get picture by {URL}")


class ImageSupplier:
    @staticmethod
    def getImage():
        try:
            return requests.get(URL, stream=True).raw
        except Exception:
            raise ImageHttpRequestFailedException()
