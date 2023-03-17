
import azure.cosmos.exceptions
from fastapi import HTTPException, status

from ..forms.models import FormularInDB
from .models import FormSubmissionCreate, FormSubmissionInDB
from ..database.cosmo_db import form_submits_container


async def validate_form_submission(form: FormularInDB, new_from_submission: FormSubmissionCreate) -> None:
    """
    Validates a new form submission, to verify if all the given form fields have been completed.

    :param form: The formular being completed
    :param new_from_submission:  The new form submission
    :raises HTTPException if one of the fields of the form has not been completed.
    :return: None
    """

    # Check to see if they send all the data the form requires
    unfilled_fields = []
    for dynamic_field in form.dynamic_fields:
        # If the field is not specified or is empty
        if dynamic_field.placeholder not in new_from_submission.completed_dynamic_fields \
                or not new_from_submission.completed_dynamic_fields[dynamic_field.placeholder]:
            unfilled_fields.append(dynamic_field.placeholder)

    if unfilled_fields:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"All fields must be specified. The following fields are missing or empty:"
                                   f" {unfilled_fields}.")


async def get_form_submission_from_db(form_submission_id: str) -> FormSubmissionInDB:
    """
    Returns the form submission from the database if it exists.

    :raises HTTPException if the form submission doesn't exist
    :param form_submission_id: The ID of the form submission
    :return: The form submission object
    """

    try:
        form_submission_dict = form_submits_container.read_item(
            item=form_submission_id,
            partition_key=form_submission_id
        )
    except azure.cosmos.exceptions.CosmosHttpResponseError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="The form submission was not found.")

    return FormSubmissionInDB(**form_submission_dict)
