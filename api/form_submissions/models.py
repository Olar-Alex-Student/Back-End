from pydantic import BaseModel


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

    class Config:
        schema_extra = {
            "example": {
                "id": "c12d3832-3c14-4922-a2b2-f8431581fa3c",
                "form_id": "fce48fed-d644-4da0-9b31-c69bf612c3c5",
                "submission_time": 1678028760,
                "completed_dynamic_fields": {
                    "cnp": 1234567890,
                    "name": "Valentin",
                    "address": "7353 South St. Braintree, MA 02184"}
            }
        }
