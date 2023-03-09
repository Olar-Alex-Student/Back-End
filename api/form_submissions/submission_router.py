from fastapi import APIRouter, Depends, Path, Request, HTTPException, status

import azure.cosmos.exceptions
from .models import FormSubmissionCreate, FormSubmissionInDB, FormSubmissionUpdate
from ..users.models import User
from ..authentication.encryption import get_current_user
from ..forms.functions import get_formular_from_db
from ..database.cosmo_db import form_submits_container
from .functions import delete_all_forms_submission

router = APIRouter(
    prefix="/api/v1/users/{user_id}/forms/{form_id}/submissions"
)


@router.post(path="/",
             tags=["form submission"])
async def add_form_submission(
        user_id: str,
        form_id: str,
        new_from: FormSubmissionCreate,
        current_user: User = Depends(get_current_user)
) -> FormSubmissionInDB:
    pass


@router.get(path="/{form_submission_id}",
            tags=["form submission"])
async def get_one_form_submission(
        user_id: str,
        form_id: str,
        form_submission_id: str,
        current_user: User = Depends(get_current_user)
) -> FormSubmissionInDB:
    # Use the form_submission_id to search for the submission
    # See if the form exists and who tries to get the submission is the owner of the form
    pass


@router.get(path="/",
            tags=["form submission"])
async def get_all_form_submissions(
        form_submission_id: str,
        user_id: str = Path(example="c6c1b8ae-44cd-4e83-a5f9-d6bbc8eeebcf",
                            description="The id of the user."),
        form_id: str = Path(example="f38f905c-caab-4565-bf49-969d0802fac4",
                            description="The name of the form"),
        current_user: User = Depends(get_current_user)

) -> FormSubmissionInDB:
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="")


@router.delete(path="/{form_submission_id}",
               tags=["form submission"])
async def delete_form_submission(
        form_submission_id: str = Path(example="6244fe72-565a-425d-aa32-83bf83af1505",
                                       description="The id of the form submission."),
        user_id: str = Path(example="c6c1b8ae-44cd-4e83-a5f9-d6bbc8eeebcf",
                            description="The id of the user."),
        form_id: str = Path(example="f38f905c-caab-4565-bf49-969d0802fac4",
                            description="The id of the form"),
        current_user: User = Depends(get_current_user)

) -> FormSubmissionInDB:
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can delete only your own data.")
        # Verifies if the owner is the form and the user are the same
    try:
        form = get_formular_from_db(form_id)
    except azure.cosmos.exceptions.CosmosResourceNotFoundError:
        form_submit = form_submits_container.delete_item(
            item=form_id,
            partition_key=form_id,
        )
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Form ''{form_id}'' does not exist."
                            )

    if form.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only delete your own forms")
        # Checks if the form belongs to the user

    form_submits = form_submits_container.read_item(
        item=form_submission_id,
        partition_key=form_submission_id,
    )

    if form_submits["form_id"] != form.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forms ids do not match")
        # Form id does not match

    form_submits_container.delete_item(
        item=form_submission_id,
        partition_key=form_submission_id,
    )
    return FormSubmissionInDB(**form_submits)


@router.delete(path="/",
               tags=["form submission"])
async def delete_all_form_submission(
        user_id: str = Path(example="c6c1b8ae-44cd-4e83-a5f9-d6bbc8eeebcf",
                            description="The id of the user."),
        form_id: str = Path(example="f38f905c-caab-4565-bf49-969d0802fac4",
                            description="The id of the form"),
        current_user: User = Depends(get_current_user)

):
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can delete only your own data.")
        # Verifies if the owner is the form and the user are the same

    return await delete_all_forms_submission(form_id, user_id)
