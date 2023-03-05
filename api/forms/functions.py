
import azure.cosmos.exceptions

from fastapi import HTTPException, status

from ..database.cosmo_db import forms_container
from .models import FormularInDB


def get_formular_from_db(form_id: str) -> FormularInDB:
    """
    Fetches the form data from the database.

    :param form_id: The ID of the form you want to get the data for.
    :return: The FormularInDB object.
    :raises HTTPException the form could not be found.
    """
    try:
        form = forms_container.read_item(
            item=form_id,
            partition_key=form_id,
        )
    except azure.cosmos.exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Form ''{form_id}'' does not exist."
                            )

    return FormularInDB(**form)


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
