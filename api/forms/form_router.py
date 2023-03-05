
import time
import uuid
import azure
import qrcode

from fastapi import APIRouter, Depends, Request, Path, Response
from ..database.cosmo_db import forms_container
from .models import FormularInDB, FormularCreate, FormularUpdate, PaginatedFormularResponse, FieldType
from ..authentication.encryption import get_current_user
from ..users.models import User
from .functions import get_tokens_from_rtf_text, get_formular_from_db
from .exceptions import *

router = APIRouter(
    prefix="/api/v1/users/{user_id}/forms"
)


@router.post(path="/",
             tags=['forms'])
async def create_new_form(
        user_id: str,
        new_from: FormularCreate,
        current_user: User = Depends(get_current_user)
) -> FormularInDB:
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

    formular = FormularInDB(id=new_form_id,
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
        updated_from: FormularUpdate,
        current_user: User = Depends(get_current_user)
) -> FormularInDB:

    # Try to see if the form exists, there is no function to only update for the CosmoDB, only upsert
    # and we don't want to create a new form with an id given by the user
    form = get_formular_from_db(form_id)

    if form.owner_id != user_id or user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can modify only your own forms.")

    form_to_save = FormularInDB(id=form_id,
                                owner_id=user_id,
                                **updated_from.dict(exclude_none=True))

    forms_container.upsert_item(form_to_save.dict(exclude_none=True))

    return form_to_save


@router.get(path="/",
            tags=['forms'])
async def get_all_user_forms(
        user_id: str,
        form_id: str,
        current_user: User = Depends(get_current_user)
) -> PaginatedFormularResponse:
    ...


@router.get(path="/{form_id}/getQR",
            tags=['forms'])
async def get_form_qr_code(
        request: Request,
        user_id: str = Path(example="c6c1b8ae-44cd-4e83-a5f9-d6bbc8eeebcf",
                            description="The id of the user."),
        form_id: str = Path(example="f38f905c-caab-4565-bf49-969d0802fac4",
                            description="The name of the form"),
        current_user: User = Depends(get_current_user),
):

    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ony the form owner can generate a QR code.")

    # Check if form exists
    get_formular_from_db(form_id)

    # TODO: add a path parameter so we can receive this link from the frontend, and then make a QR code
    # TODO: ,right now it just sends the user to an api call in the backend, it should send them to something like /view

    # Create a link to the access a form
    current_url = request.url.path
    url_to_send = '/'.join(current_url.split('/')[:-1])

    # Converts the link in a qr code and saves the image
    img = qrcode.make(url_to_send)
    img.save("form_qr_code.png")

    # Opens the image in byte format, since that's what we can send
    file = open("form_qr_code.png", "rb")

    return Response(content=file.read(), media_type="image/png")


@router.get(path="/{form_id}",
            tags=['forms'])
async def get_form_data(
        user_id: str = Path(example="c6c1b8ae-44cd-4e83-a5f9-d6bbc8eeebcf",
                            description="The id of the user."),
        form_id: str = Path(example="f38f905c-caab-4565-bf49-969d0802fac4",
                            description="The name of the form"),
        current_user: User = Depends(get_current_user),
) -> FormularInDB:

    # All users should be allowed to fetch a form, so they can complete it
    return get_formular_from_db(form_id)


@router.delete(path="/{form_id}",
               tags=['forms'])
async def delete_form(
        user_id: str = Path(example="c6c1b8ae-44cd-4e83-a5f9-d6bbc8eeebcf",
                            description="The id of the user."),
        form_id: str = Path(example="f38f905c-caab-4565-bf49-969d0802fac4",
                            description="The name of the form"),
        current_user: User = Depends(get_current_user),

) -> FormularInDB:

    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can delete only your own data.")
        # Verifies if the owner if the form and the user are the same

    form = get_formular_from_db(form_id)

    if form.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can delete only your own forms.")
        # Checks if the form belongs to the user

    forms_container.delete_item(
        item=form_id,
        partition_key=form_id,
    )
    return form
