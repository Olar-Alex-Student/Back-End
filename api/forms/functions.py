from ..database.cosmo_db import forms_container


def get_tokens_from_rtf_text(text: str):
    tokens = []
    token = ""

    for letter in text:
        if letter == '<':
            token = ''

        if letter == '>' and len(token) > 1:
            tokens.append(token[1:])

        token += letter

    return tokens
