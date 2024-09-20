import re

PROMPTS = '0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
VALID_SHORT_ID = re.compile(r'^[a-zA-Z0-9]{1,16}$')

