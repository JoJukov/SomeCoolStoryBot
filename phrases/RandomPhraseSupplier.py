import random
from .phrasesTemplates import *


class _RandomPhraseSupplierMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class RandomPhraseSupplier(metaclass=_RandomPhraseSupplierMeta):
    def get_random_phrase_beggining(self) -> str:
        return random.choice(list(BeginningOfTheStoryPhraseEnum)).value

    def get_random_phrase_welcome(self) -> str:
        return random.choice(list(WelcomePhraseEnum)).value
