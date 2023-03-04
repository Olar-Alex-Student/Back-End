import uuid
import uuid as uuid_pkg

from pydantic import BaseModel, Field
from fastapi import Path
from enum import Enum


class AccountType(str, Enum):
    individual = "individual"
    company = "company"
    public_institution = "public_institution"


class NewUser(BaseModel):
    name: str
    email: str
    password: str
    account_type: AccountType
    fiscal_code: str = ""
    address: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Vizitiu Valentin",
                "email": "poggers1234@pogmail.com",
                "password": "1234",
                "account_type": AccountType.individual.value,
                "address": "7353 South St. Braintree, MA 02184"
            }
        }


class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4)
    name: str
    email: str
    password: str
    account_type: AccountType
    fiscal_code: str = ""
    address: str

    class Config:
        schema_extra = {
            "example": {
                "id": "f903e408-5664-4aba-8b37-20f3c2a49725",
                "name": "Vizitiu Valentin",
                "email": "poggers1234@pogmail.com",
                "password": "123hashed-password321",
                "account_type": AccountType.individual.value,
                "address": "7353 South St. Braintree, MA 02184",
                "fiscal_code": "1234567890",
            }
        }


class UpdatedUser(BaseModel):
    id: str = Field(default_factory=uuid.uuid4)
    account_type: AccountType = Field(default='', description="The new account name of the user")
    name: str = Field(default='')
    fiscal_code: str = Field(default='')
    address: str = Field(default='')
    email: str = Field(default='')
    password: str = Field(default='')

    class Config:
        schema_extra = {
            "example": {
                "name": "Olar Alex",
                "email": "poggers1234@pogmail.com",
                "account_type": AccountType.individual.value,
                "address": "7353 South St. Braintree, MA 02184",
                "password": "1234"
            }
        }
