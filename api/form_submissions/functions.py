import azure

import azure.cosmos.exceptions
from fastapi import HTTPException, status

from ..forms.models import FormularInDB
from .models import FormSubmissionInDB, FormSubmissionCreate
from ..database.cosmo_db import form_submits_container
from ..forms.functions import get_formular_from_db


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


async def delete_all_forms_submission(form_id: str, user_id: str):
    query = """SELECT form.id FROM c form WHERE form.form_id = @form_id"""

    params = [dict(name="@form_id", value=form_id)]

    results = form_submits_container.query_items(query=query,
                                                 parameters=params,
                                                 enable_cross_partition_query=True)

    items = list(results)
    # Returns a list of all the form submits that are created from the same form

    result = 0

    form = None

    try:
        form = get_formular_from_db(form_id)
    except azure.cosmos.exceptions.CosmosResourceNotFoundError:
        pass
    # Verifies if the form exists

    if form and form.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only delete your own forms")
        # Checks if the form belongs to the user

    for submitted_form_id in items:
        form_submits_container.delete_item(
            item=submitted_form_id["id"],
            partition_key=submitted_form_id["id"],
        )

        result += 1
        # Deletes all the form submits and returns the number that it has deleted

    return f"Deleted {result} forms with success."
