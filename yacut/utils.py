import random

from .constants import PROMPTS


def get_unique_short_id():
    listprompts = list(PROMPTS)
    randprompts = ''.join([random.choice(listprompts) for x in range(6)])
    return randprompts
