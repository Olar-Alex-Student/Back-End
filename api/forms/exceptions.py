from fastapi import HTTPException, status

invalid_delete_form_date = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                         detail="'delete_form_date' is smaller than current time. This value should "
                                                "be the epoch second when the form should be removed.")

missing_scan_document_type = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                           detail="Missing 'scan_document_type' for one of the sections. Use 'None' if "
                                                  "you don't want any document.")

missing_section_text = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                     detail="Missing 'text' for one of the sections.")


class UnspecifiedField(HTTPException):
    def __init__(self, field: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail=f"Unspecified field '{field}' found in text section.")


class NoFieldOptionsProvided(HTTPException):
    def __init__(self, field_name: str, field_type: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail=f"No options provided for '{field_type}' field for '{field_name}'.")


class NoFieldKeywordsProvided(HTTPException):
    def __init__(self, field_name: str, field_type: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail=f"No options provided for '{field_type}' field for '{field_name}'.")


class MissingFieldType(HTTPException):
    def __init__(self, field: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail=f"Missing or invalid 'type' parameter for field '{field}'.")


class MissingDocumentKeywords(HTTPException):
    def __init__(self, field: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail=f"Missing or invalid 'keywords' parameter for field '{field}'.")

