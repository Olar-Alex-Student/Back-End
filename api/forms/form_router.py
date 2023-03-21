
import uuid

from fastapi import APIRouter, Depends, Path
from ..database.cosmo_db import forms_container
from .models import FormularInDB, FormularCreate, FormularUpdate, PaginatedFormularResponse
from ..authentication.encryption import get_current_user
from ..users.models import User
from .functions import get_formular_from_db, get_short_user_forms_from_db, validate_form_data
from .exceptions import *
from ..form_submissions.functions import delete_all_forms_submission
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
                                   " user that's logged in.")

    # Validate the given form data
    validate_form_data(new_from)

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

    validate_form_data(updated_from)

    form_to_save = FormularInDB(id=form_id,
                                owner_id=user_id,
                                **updated_from.dict(exclude_none=True))

    forms_container.upsert_item(form_to_save.dict(exclude_none=True))

    return form_to_save


@router.get(path="/",
            tags=['forms'])
async def get_all_user_forms_description(
        user_id: str,
        current_user: User = Depends(get_current_user)
) -> PaginatedFormularResponse:

    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can view only your own forms.")

    forms = get_short_user_forms_from_db(user_id)

    return forms


@router.get(path="/{form_id}",
            tags=['forms'])
async def get_form_data(
        user_id: str = Path(example="c6c1b8ae-44cd-4e83-a5f9-d6bbc8eeebcf",
                            description="The id of the user."),
        form_id: str = Path(example="67b64054-db84-489a-af92-fe87f9be9899",
                            description="The name of the form"),
) -> FormularInDB:

    # All users should be allowed to fetch a form, so they can complete it
    return get_formular_from_db(form_id)


@router.delete(path="/{form_id}",
               tags=['forms'])
async def delete_form(
        user_id: str = Path(example="c6c1b8ae-44cd-4e83-a5f9-d6bbc8eeebcf",
                            description="The id of the user."),
        form_id: str = Path(example="67b64054-db84-489a-af92-fe87f9be9899",
                            description="The id of the form"),
        current_user: User = Depends(get_current_user),

) -> FormularInDB:

    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can delete only your own data.")
        # Verifies if the owner is the form and the user are the same

    form = get_formular_from_db(form_id)
    # Retrieves the form from the database

    if form.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can delete only your own forms.")
        # Checks if the form belongs to the user

    await delete_all_forms_submission(form_id, user_id)
    # Before deleting the form it will delete all the form submissions

    forms_container.delete_item(
        item=form_id,
        partition_key=form_id,
    )
    # Deletes the form from the database and returns it

    return form
