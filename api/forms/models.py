from enum import Enum

from pydantic import BaseModel,  validator
from typing import Optional


class ScannableDocuments(str, Enum):
    student_card = 'student_card'
    identity_card = 'identity_card'
    passport = 'passport'
    birth_certificate = 'birth_certificate'
    vehicle_identity_card = 'vehicle_identity_card'
    driver_license = 'driver_license'
    any = 'any'


valid_field_types = {'text', 'number', 'decimal', 'date', 'single-choice', 'multiple-choice'}


class FieldType(str, Enum):
    text = 'text'
    number = 'number'
    decimal = 'decimal'
    data = 'date'
    single_choice = 'single-choice'
    multiple_choice = 'multiple-choice'


class DocumentSection(BaseModel):
    scan_document_type: ScannableDocuments
    text: str


class DynamicFieldData(BaseModel):
    placeholder: str
    type: FieldType
    mandatory: bool
    keywords: Optional[list[str]] = None
    options: Optional[list[str]] = None


class NewFormular(BaseModel):
    title: str
    delete_form_date: int
    sections: list[DocumentSection]
    dynamic_fields: list[DynamicFieldData]

    class Config:
        schema_extra = {
            "example": {
                "title": "Document Permis Conducere",
                "delete_form_date": "1677937850",
                "sections": [
                    {
                        "scan_document_type": "student_card",
                        "text": "Studentul <nume> , din grupa , anul <anul>. Aleg optiunea <opt1>."
                    },
                    {
                        "scan_document_type": "identity_card",
                        "text": "Cu CNP <cnp>, seria , nr."
                    }
                ],
                "dynamic_fields": [
                    {"placeholder": "nume", "type": "text", "keywords": ["name", "nume", "first_name"], "mandatory": True},
                    {"placeholder": "cnp", "type": "number", "keywords": ["cnp", "security number"], "mandatory": True},
                    {"placeholder": "anul", "type": "single-choice", "mandatory": True, "options": ["1", "2", "3", "4"]},
                    {"placeholder": "opt1", "type": "multiple-choice", "mandatory": True, "options": ["Creoin", "Pix", "Caiet", "Carte"]},
                ]
            }
        }


class Formular(NewFormular):
    id: str
    owner_id: str

    class Config:
        schema_extra = {
            "example": {
                "id": "9dbfce20-a68c-40e4-ae42-d75f73cf2a6c",
                "owner_id": "1398589c-1e13-48b5-9c89-d2c8ed26fcaf",
                "title": "Document Permis Conducere",
                "delete_form_date": "1677937850",
                "sections": [
                    {
                        "scan_document_type": "student_card",
                        "text": "Studentul <nume> <prenume>, din grupa <grupa>, anul <anul>. Aleg optiunea <opt1>."
                    },
                    {
                        "scan_document_type": "identity_card",
                        "text": "Cu CNP <cnp>, seria <seria>, nr <nr_carte_identitate>."
                    }
                ],
                "dynamic_fields": [
                    {"placeholder": "nume", "type": "text", "keywords": ["name", "nume", "first_name"], "mandatory": True},
                    {"placeholder": "cnp", "type": "number", "keywords": ["cnp", "security number"], "mandatory": True},
                    {"placeholder": "anul", "type": "single-choice", "mandatory": True, "options": ["1", "2", "3", "4"]},
                    {"placeholder": "opt1", "type": "multiple-choice", "mandatory": True, "options": ["Creoin", "Pix", "Caiet", "Carte"]},
                ]
            }
        }