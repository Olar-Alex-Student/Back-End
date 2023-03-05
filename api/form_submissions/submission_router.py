from fastapi import APIRouter, Depends

from .models import FormSubmissionCreate, FormSubmissionInDB, FormSubmissionUpdate
from ..users.models import User
from ..authentication.encryption import get_current_user

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
