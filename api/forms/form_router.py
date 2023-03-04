import json
import time
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from ..database.cosmo_db import forms_container
from .models import Formular, NewFormular, FieldType
from ..users.models import User
from ..authentication.encryption import get_current_user
from .exceptions import *

router = APIRouter(
    prefix="/api/v1/users/{user_id}/forms"
)


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


@router.post(path="/",
             tags=['forms'])
async def create_new_form(
        user_id: str,
        new_from: NewFormular,
        current_user: User = Depends(get_current_user)
) -> Formular:
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Path user_id does not match logged in user's id. You can create forms only for the"
                                   " use that's logged in.")

    # Validate the given form data
    current_time = time.time()

    if new_from.delete_form_date < current_time:
        raise invalid_delete_form_date

    valid_fields = []

    for field_data in new_from.dynamic_fields:
        valid_fields.append(field_data.placeholder)

        if field_data.type.value in (FieldType.single_choice.value, FieldType.multiple_choice.value) \
                and not field_data.options:
            raise NoFieldOptionsProvided(field_data.placeholder, field_data.type.value)

        if field_data.type.value not in (FieldType.single_choice.value, FieldType.multiple_choice.value) \
                and not field_data.keywords:
            raise NoFieldKeywordsProvided(field_data.placeholder, field_data.type.value)

    for section in new_from.sections:
        section_fields = get_tokens_from_rtf_text(section.text)

        for field in section_fields:
            if field not in valid_fields:
                raise UnspecifiedField(field)

    new_form_id = str(uuid.uuid4())

    formular = Formular(id=new_form_id,
                        owner_id=user_id,
                        **new_from.dict())

    # The new item created doesn't include empty values
    forms_container.create_item(
        formular.dict(exclude_none=True)
    )

    return formular


@router.put(path="/{form_id}",
            tags=['forms'])
async def edit_form_data(
        user_id: str,
        form_id: str,
):
    pass


@router.get(path="/",
            tags=['forms'])
async def get_all_user_forms(
        user_id: str
):
    pass


@router.get(path="/{form_id}",
            tags=['forms'])
async def get_form_data(
        user_id: str,
        form_id: str,
):
    form = forms_container.read_item(
        item=form_id,
    )


@router.delete(path="/{form_id}",
               tags=['forms'])
async def create_new_form(
        user_id: str,
        form_id: str,
):
    pass
