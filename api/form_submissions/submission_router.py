import datetime
import time
import uuid

import azure.cosmos.exceptions
from fastapi import APIRouter, Depends, Path, HTTPException, Query, status

from .models import FormSubmissionInDB, FormSubmissionCreate, FormSubmissionUpdate, sorting_Order, sort_Order_to_bool
from ..users.models import User
from ..authentication.encryption import get_current_user
from .functions import validate_form_submission, get_form_submission_from_db, delete_all_forms_submission
from ..forms.functions import get_formular_from_db
from ..database.cosmo_db import form_submits_container

SECONDS_IN_ONE_DAY = 60 * 60 * 24

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

    current_time = time.time()
    form_submission_expiration_date = current_time + form.data_retention_period * SECONDS_IN_ONE_DAY

    new_submission_id = str(uuid.uuid4())

    new_from_submission = FormSubmissionInDB(
        id=new_submission_id,
        form_id=form_id,
        user_that_completed_id=current_user.id,
        submission_expiration_time=form_submission_expiration_date,
        submission_creation_time=current_time,
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
    # Only the completed dynamic fields can be updated
    form_submission.completed_dynamic_fields = updated_from_submission.completed_dynamic_fields

    # Update the submission
    form_submits_container.upsert_item(
        form_submission.dict(exclude_none=True)
    )

    return form_submission


@router.get(path="/{form_submission_id}",
            tags=["form submission"])
async def get_one_form_submission(
        form_submission_id: str = Path(example="011b0b3d-ebbf-4ce8-9216-4d5f6e12c134",
                                       description="The id of the form submission."),
        user_id: str = Path(example="c6c1b8ae-44cd-4e83-a5f9-d6bbc8eeebcf",
                            description="The id of the user."),
        form_id: str = Path(example="f38f905c-caab-4565-bf49-969d0802fac4",
                            description="The id of the form"),
        current_user: User = Depends(get_current_user)

) -> FormSubmissionInDB:
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can delete only your own data.")
        # Verifies if the owner of the form and the user are the same

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
    # Verifies if the form and the form submission exist in the database

    if form.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only delete your own forms")
        # Checks if the form belongs to the user

    form_submits = form_submits_container.read_item(
        item=form_submission_id,
        partition_key=form_submission_id,
    )
    # Reads the form submit from the database

    if form_submits["form_id"] != form.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forms ids do not match")
        # Raise an error if id does not match

    return FormSubmissionInDB(**form_submits)

    # Use the form_submission_id to search for the submission.
    # Make's sure if the form exists and who tries to get the submission is the owner of the form.
    pass


@router.get(path="",
            tags=["form submission"])
async def get_all_form_submissions_by_form_data(
        sort_order: sorting_Order = Query(
            default=sorting_Order.ascending,
            description="The order of the form submission, sorted by the submission time."),
        string_to_find: str = Query(default='',
                                    example="Valentin",
                                    description="A string to search for in the form submission completed values."),
        submitted_during: str = Query(default='',
                                      example="12-19-03-2023",
                                      description="The date and time when the submission was created."
                                                  " Specify them as hh-dd-mm-yyyy."),
        user_id: str = Path(example="c6c1b8ae-44cd-4e83-a5f9-d6bbc8eeebcf",
                            description="The id of the user."),
        form_id: str = Path(example="67b64054-db84-489a-af92-fe87f9be9899",
                            description="The id of the form"),
        current_user: User = Depends(get_current_user)

) -> list[FormSubmissionInDB]:
    # Verify if it's the form owner
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You can't access other's people submissions.")

    # Verify if the form still exists
    # If it doesn't exist we can delete all it's submissions
    try:
        form = get_formular_from_db(form_id)
    except azure.cosmos.exceptions.CosmosResourceNotFoundError:
        await delete_all_forms_submission(form_id, user_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Form ''{form_id}'' does not exist."
                            )

    # Verify if its the form owner
    if form.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You can't access other's people submissions.")

    # Query all the form submissions
    query = """
SELECT 

submission.id, 
submission.form_id, 
submission.completed_dynamic_fields, 
submission.user_that_completed_id, 
submission.submission_creation_time, 
submission.submission_expiration_time 

FROM c submission WHERE submission.form_id = @form_id"""

    params = [dict(name="@form_id", value=form_id)]

    results = form_submits_container.query_items(query=query,
                                                 parameters=params,
                                                 enable_cross_partition_query=True)

    # Sort the submissions by the expiration time
    form_submissions_list = sorted(list(results),
                                   key=lambda x: x["submission_expiration_time"],
                                   reverse=sort_Order_to_bool[sort_order.value])

    # If they specified a string to find, remove the ones that don't meet the criteria
    if string_to_find:
        mach_list = []

        for submission in form_submissions_list:
            for i, field in enumerate(submission["completed_dynamic_fields"]):

                # The requirements of the app say that the search string should be only between the first
                # 5 completed fields of the submission
                if i >= 5:
                    break

                if string_to_find in str(submission["completed_dynamic_fields"][field]):
                    mach_list.append(submission)
    else:
        mach_list = form_submissions_list

    # Give only the submissions that happened during this time
    if submitted_during:
        form_submissions_list = mach_list
        mach_list = []

        hour, day, month, year = [int(i) if i.isnumeric() else -1 for i in submitted_during.split('-')]

        for submission in form_submissions_list:
            submitted_at = datetime.datetime.fromtimestamp(submission['submission_creation_time'])

            # For all the time specifiers, if they are not -1 (this means they were given by the user),
            # verify if the submission was created during this time
            if 0 <= hour != submitted_at.hour:
                continue

            if 0 <= day != submitted_at.day:
                continue

            if 0 <= month != submitted_at.month:
                continue

            if 0 <= year != submitted_at.year:
                continue

            mach_list.append(submission)

    return mach_list


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
        # Verifies if the owner of the form and the user are the same
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
    # Verifies if the form exists in the database

    if form.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only delete your own forms")
        # Checks if the form belongs to the user

    form_submits = form_submits_container.read_item(
        item=form_submission_id,
        partition_key=form_submission_id,
    )
    # Reads the form submit from the database

    if form_submits["form_id"] != form.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forms ids do not match")
        # Form id does not match

    form_submits_container.delete_item(
        item=form_submission_id,
        partition_key=form_submission_id,
    )
    # Deletes the form submit and returns it
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
        # Verifies if the owner of the form and the user are the same

    return await delete_all_forms_submission(form_id, user_id)
