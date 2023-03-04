"""- POST create new form (see assist docs for the data a form has)
--Careful with forms here, how to save the fields they have and all.
- PUT update a form
- GET all forms of a user"""
from fastapi import APIRouter
from ..database.cosmo_db import forms_container

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
async def create_new_form(
        user_id: str,
        form_id: str,
):
    pass
    #asdasdsdadasdasd
