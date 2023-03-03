"""
Check the links I provided to learn more about WHY I did something in that way
"""

from pydantic import BaseModel, Field
from fastapi import Path
from enum import Enum


# https://fastapi.tiangolo.com/tutorial/path-params/#create-an-enum-class
class AccountType(str, Enum):
    individual = "individual"
    company = "company"
    public_institution = "public_institution"


class User(BaseModel):
    account_type: AccountType
    name: str
    fiscal_code: str = None
    address: str
    email: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Vizitiu Valentin",
                "email": "poggers1234@pogmail.com",
                "account_type": AccountType.individual.value,
                "address": "7353 South St. Braintree, MA 02184",
                "fiscal_code": "",
            }
        }


class UpdatedUser(BaseModel):
    account_type: AccountType = Field(default='', description="The new account name of the user")
    name: str = Field(default='')
    fiscal_code: str = Field(default='')
    address: str = Field(default='')
    email: str = Field(default='')
    password: str = Field(default='')

    class Config:
        schema_extra = {
            "example": {
                "email": "poggers1234@pogmail.com",
                "account_type": AccountType.individual.value,
                "address": "7353 South St. Braintree, MA 02184",
                "fiscal_code": "",
                "password": "1234"
            }
        }


class UserInDatabase(User):
    password: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Vizitiu Valentin",
                "email": "poggers1234@pogmail.com",
                "account_type": AccountType.individual.value,
                "address": "7353 South St. Braintree, MA 02184",
                "fiscal_code": "",
                "password": "4321"
            }
        }