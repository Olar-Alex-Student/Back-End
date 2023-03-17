import time
import azure.cosmos.exceptions

from fastapi import HTTPException, status

from ..database.cosmo_db import forms_container
from .models import FormularInDB, FormularCreate, PaginatedFormularResponse, FieldType
from .exceptions import invalid_delete_form_date, NoFieldOptionsProvided, NoFieldKeywordsProvided, UnspecifiedField


SECONDS_IN_ONE_DAY = 24 * 60 * 60
SECONDS_IN_SIXTY_DAY = SECONDS_IN_ONE_DAY * 60


def validate_form_data(form: FormularCreate):
    """Takes a form and validates if it's data is correct."""

    # Delete timestamp should be between 1 and 60 days
    current_time = time.time()
    min_retention_time = current_time + SECONDS_IN_ONE_DAY
    max_retention_time = current_time + SECONDS_IN_SIXTY_DAY

    if not min_retention_time < form.delete_form_date < max_retention_time:
        raise invalid_delete_form_date

    valid_fields = []

    # individuals should NOT have fiscal code, but companies and public institutions should
    for field_data in form.dynamic_fields:
        valid_fields.append(field_data.placeholder)

        if field_data.type.value in (FieldType.single_choice.value, FieldType.multiple_choice.value) \
                and not field_data.options:
            raise NoFieldOptionsProvided(field_data.placeholder, field_data.type.value)

        if field_data.type.value not in (FieldType.single_choice.value, FieldType.multiple_choice.value) \
                and not field_data.keywords:
            raise NoFieldKeywordsProvided(field_data.placeholder, field_data.type.value)

    # All placeholder keywords declared in the RTF text sections must be specified in the dynamic fields
    for section in form.sections:
        section_fields = get_tokens_from_rtf_text(section.text)

        for field in section_fields:
            if field not in valid_fields:
                raise UnspecifiedField(field)


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
                            detail=f"Form '{form_id}' does not exist."
                            )

    return FormularInDB(**form)


def get_short_user_forms_from_db(user_id: str) -> PaginatedFormularResponse:
    """
    Returns the id, title and expiration date of all the forms of the user.

    :param user_id: The id of the user to get the forms of

    :return: The list of forms
    """

    # When getting the user it will be possible to search with both name or email
    # So we can each by both at once, and works correctly

    query = """SELECT form.id, form.title, form.delete_form_date
                    FROM c form 
                    WHERE form.owner_id = @user_id"""

    params = [dict(name="@user_id", value=user_id)]

    results = forms_container.query_items(query=query,
                                          parameters=params,
                                          enable_cross_partition_query=True)

    items = list(results)

    return PaginatedFormularResponse(form_list=items)


def get_tokens_from_rtf_text(text: str):
    """
    Example: "Studentul <nume>, <prenume>, <grupa>" => ['nume', 'prenume', 'grupa']

    :param text: Text in RFT format
    :return: a list of tokens extracted from the text
    """
    tokens = []
    token = ""

    for letter in text:
        if letter == '<':
            token = ''

        if letter == '>' and len(token) > 1:
            tokens.append(token[1:])

        token += letter

    return tokens
