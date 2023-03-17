import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from .models import FormSubmissionCreate, FormSubmissionInDB, FormSubmissionUpdate
from ..users.models import User
from ..authentication.encryption import get_current_user
from ..forms.functions import get_formular_from_db
from ..database.cosmo_db import form_submits_container
from .functions import validate_form_submission, get_form_submission_from_db

router = APIRouter(
    prefix="/api/v1/users/{user_id}/forms/{form_id}/submissions"
)


@router.post(path="/",
             tags=["form submission"])
async def add_form_submission(
        user_id: str,
        form_id: str,
        new_from_submission: FormSubmissionCreate,
        current_user: User = Depends(get_current_user)
) -> FormSubmissionInDB:
    # Check if form exists
    form = get_formular_from_db(form_id)

    # No need to check if it's the owner of the form, as anyone can add a submission

    # Validate the new submission
    await validate_form_submission(form, new_from_submission)

    new_submission_id = str(uuid.uuid4())

    new_from_submission = FormSubmissionInDB(
        id=new_submission_id,
        form_id=form_id,
        user_that_completed_id=current_user.id,
        **new_from_submission.dict()
    )

    form_submits_container.create_item(
        new_from_submission.dict(exclude_none=True)
    )

    return new_from_submission


@router.put(path="/{form_submission_id}",
            tags=["form submission"])
async def update_form_submission(
        user_id: str,
        form_id: str,
        form_submission_id: str,
        updated_from_submission: FormSubmissionUpdate,
        current_user: User = Depends(get_current_user)
) -> FormSubmissionInDB:
    # Check if form exists
    form = get_formular_from_db(form_id)

    # Verify if the submission exists
    # Raises an exception if the submission does not exist
    form_submission = await get_form_submission_from_db(form_submission_id)

    # Verify if they are allowed to update the submission
    if form.owner_id != current_user.id and form_submission.user_that_completed_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this submission"
        )

    # Validate the new submission
    await validate_form_submission(form, updated_from_submission)

    # Create the updated submission
    updated_from_submission = FormSubmissionInDB(
        id=form_submission_id,
        form_id=form_id,
        user_that_completed_id=form_submission.user_that_completed_id,
        **updated_from_submission.dict()
    )

    # Update the submission
    form_submits_container.upsert_item(
        updated_from_submission.dict(exclude_none=True)
    )

    return updated_from_submission


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
        user_id: str,
        form_id: str,
        current_user: User = Depends(get_current_user)
) -> FormSubmissionInDB:
    pass


@router.delete(path="/{form_submission_id}",
               tags=["form submission"])
async def delete_form_submission(
        user_id: str,
        form_id: str,
        form_submission_id: str,
        current_user: User = Depends(get_current_user)
) -> FormSubmissionInDB:
    pass


@router.delete(path="/",
               tags=["form submission"])
async def delete_all_form_submission(
        user_id: str,
        form_id: str,
        current_user: User = Depends(get_current_user)
) -> FormSubmissionInDB:
    pass
