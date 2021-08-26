import random
from .phrasesTemplates import *


class RandomPhraseSupplier:
    @staticmethod
    def get_random_phrase_beggining() -> str:
        return random.choice(list(BeginningOfTheStoryPhraseEnum)).value

    @staticmethod
    def get_random_phrase_welcome() -> str:
        return random.choice(list(WelcomePhraseEnum)).value
