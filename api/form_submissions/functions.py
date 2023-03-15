import azure
import time

from fastapi import HTTPException, status
from ..database.cosmo_db import form_submits_container
from ..forms.functions import get_formular_from_db
from ..forms.functions import invalid_delete_form_date
from .models import FormSubmissionCreate


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

# def validate_form_submission_data(form: FormSubmissionCreate):
