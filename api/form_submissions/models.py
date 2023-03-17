from pydantic import BaseModel
from enum import Enum


class FormSubmissionCreate(BaseModel):
    submission_time: int
    completed_dynamic_fields: dict

    class Config:
        schema_extra = {
            "example": {
                "submission_time": 1678028760,
                "completed_dynamic_fields": {
                    "cnp": 1234567890,
                    "name": "Valentin",
                    "address": "7353 South St. Braintree, MA 02184"}
            }
        }


class FormSubmissionUpdate(FormSubmissionCreate):
    """Data for the updated form"""
    pass


class FormSubmissionInDB(FormSubmissionCreate):
    id: str
    form_id: str
    user_that_completed_id: str

    class Config:
        schema_extra = {
            "example": {
                "id": "c12d3832-3c14-4922-a2b2-f8431581fa3c",
                "form_id": "fce48fed-d644-4da0-9b31-c69bf612c3c5",
                "user_that_completed_id": "2a2e6826-0e2f-4b99-880e-32dfef06c5ce",
                "submission_time": 1678028760,
                "completed_dynamic_fields": {
                    "cnp": 1234567890,
                    "name": "Valentin",
                    "address": "7353 South St. Braintree, MA 02184"}
            }
        }


class sorting_Order(str, Enum):
    ascending = "ascending"
    descending = "descending"


sort_Order_to_bool = {"ascending": True, "descending": False}
