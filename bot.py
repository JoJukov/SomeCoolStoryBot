import time

from schedule import every, repeat, run_pending
from typing import Final

from balaboba import Balaboba
from img import ImageSupplier
from phrases import RandomPhraseSupplier
from vk import VkPoster, VkAuth

VK_GROUP_ID: Final = 206741940

poster = VkPoster(VkAuth.fromPrompt(), VK_GROUP_ID)
balaboba = Balaboba()
img = ImageSupplier()
phrases = RandomPhraseSupplier()


def getTextToPost():
    hello = balaboba.generate(phrases.get_random_phrase_welcome())
    begin = balaboba.generate(phrases.get_random_phrase_beggining())
    return f"{hello}\n\n\n{begin}"


def getPhotoToPost():
    return img.getImage()


@repeat(every().hour.at(":00"))
def job():
    poster.post(getTextToPost(), getPhotoToPost())


while True:
    run_pending()
    time.sleep(30)
