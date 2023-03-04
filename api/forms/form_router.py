"""- POST create new form (see assist docs for the data a form has)
--Careful with forms here, how to save the fields they have and all.
- PUT update a form
- GET all forms of a user"""
from fastapi import APIRouter, Path, Depends, HTTPException, Depends, status
from ..database.cosmo_db import forms_container
from ..authentication.encryption import get_current_user
from ..users.models import User
import azure

router = APIRouter(
    prefix="/api/v1/users/{user_id}/forms"
)


@router.post(path="/",
             tags=['forms'])
async def create_new_form(
        user_id: str
):
    pass


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
async def delete_form(
        user_id: str = Path(example="c6c1b8ae-44cd-4e83-a5f9-d6bbc8eeebcf",
                            description="The id of the user."),
        form_id: str = Path(example="f38f905c-caab-4565-bf49-969d0802fac4",
                            description="The name of the form"),
        current_user: User = Depends(get_current_user),

) -> None:
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can delete only your own data.")
        # Verifies if the owner if the form and the user are the same

    try:
        form = forms_container.read_item(
            item=form_id,
            partition_key=form_id,
        )

        if form["owner_id"] != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can delete only your own data.")
            # Checks if the form belongs to the user

    except azure.cosmos.exceptions.CosmosResourceNotFoundError:  # type:ignore
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Form ''{form_id}'' does not exist.")
        # If a form does not exist it can't be deleted
    forms_container.delete_item(
        item=form_id,
        partition_key=form_id,
    )
    return form
