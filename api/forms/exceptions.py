from fastapi import HTTPException, status

invalid_data_retention_period = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="'data_retention_period' should should be between 1 and 60.")


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
