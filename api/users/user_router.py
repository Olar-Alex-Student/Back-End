"""
Author: Vizitiu Valentin Iulian
License: CC0 “No Rights Reserved”
Link: https://creativecommons.org/publicdomain/zero/1.0/

You are free to copy, modify and use the code in any way. I am not responsible for what you use it for.
"""
import uuid

from fastapi import APIRouter, HTTPException, Body, Depends, Path, status

from .models import User, UpdatedUser, NewUser, AccountType
from .functions import get_user_by_email_or_name
from ..database.cosmo_db import users_container
from ..authentication.encryption import get_current_user, get_password_hash

router = APIRouter(
    prefix="/api/v1/users"
)


@router.post(path="/",
             tags=["users"],
             description="Create a new user.")
async def create_new_user(
        new_user: NewUser = Body(title="A JSON with the initial user data. All fields are "
                                       "mandatory, except fiscal code, only companies should have this.")
) -> User:
    # Anyone can create a new user.
    # In a real application, they will need to verify their email and solve a captcha

    if len(new_user.name) < 3:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Account name must be at least 3 characters long.")

    # Cannot set fiscal code for individual accounts
    if new_user.fiscal_code and new_user.account_type == AccountType.individual.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Cannot set 'fiscal code' for individuals.")

    elif not new_user.fiscal_code and new_user.account_type != AccountType.individual.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Fiscal code for {new_user.account_type} is empty.")

    # Try to see if the user already exists
    user = get_user_by_email_or_name(email=new_user.email,
                                     account_name=new_user.name)

    # If this is not empty, then a user with that name or email exists
    if user:
        if user['name'] == new_user.name:
            detail = f"User with the name '{new_user.name}' already exists."
        else:
            detail = f"User with the email '{new_user.email}' already exists."

        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)

    # Hash the user password
    new_user.password = get_password_hash(new_user.password)
    new_user_id = str(uuid.uuid4())

    new_user = User(id=new_user_id, **new_user.dict())

    # Delete the empty fiscal code if the user is an individual
    if not new_user.fiscal_code:
        del new_user.fiscal_code

    users_container.create_item(new_user.dict())

    return new_user


@router.get(path="/{user_id}",
            tags=["users"],
            description="Get all of the user's data")
async def get_current_user(
        user_id: str = Path(example="f903e408-5664-4aba-8b37-20f3c2a49725",
                            description="The id of the user."),
        current_user: User = Depends(get_current_user)
) -> User:

    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You can only get the data of the user that is currently logged in.")

    return current_user


@router.put(path="/{user_id}",
            tags=["users"],
            description="Update any of the user fields.\n"
                        "In the body give only the values you wish to update.\n"
                        "⚠ You cannot update the user's account name.\n")
async def update_user(
        updated_user: UpdatedUser,
        current_user: User = Depends(get_current_user),
        user_id: str = Path(example="Vizitiu Valentin",
                            description="The email or name of the user."),
) -> UpdatedUser:

    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can modify only your own data.")

    # Hash the new password if needed
    if updated_user.password:
        updated_user.password = get_password_hash(updated_user.password)

    # For the empty values in the updated user, set them the same as the current user's data,
    # so they are not modified
    for key, value in updated_user.dict().items():
        if not value:
            setattr(updated_user, key, getattr(current_user, key))

    # Cannot change account type
    if current_user.account_type != updated_user.account_type:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="'account type' cannot be updated.")

    # Cannot set fiscal code for individual accounts
    if updated_user.fiscal_code and current_user.account_type == AccountType.individual.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot set 'fiscal code' for individuals.")

    elif not updated_user.fiscal_code and updated_user.account_type != AccountType.individual.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Fiscal code for {updated_user.account_type} is empty.")

    # If they modified the email or account name, check if one already exists
    if updated_user.email != current_user.email:
        user = get_user_by_email_or_name(email=updated_user.email)

        if user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User with the email '{updated_user.email}' already exists.")

    elif updated_user.name != current_user.name:
        user = get_user_by_email_or_name(account_name=updated_user.name)

        if user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User with the name '{updated_user.name}' already exists.")

    # Delete empty fiscal code, if it's the case
    if not updated_user.fiscal_code:
        del updated_user.fiscal_code

    updated_user.id = current_user.id

    # Now we can save the updated data
    users_container.upsert_item(updated_user.dict())

    return updated_user


@router.delete(path="/{user_id}",
               tags=["users"],
               description="Delete your account.")
async def delete_user(
        user_id: str = Path(example="Vizitiu Valentin",
                            description="The email or name of the user."),
        current_user: User = Depends(get_current_user)
) -> None:

    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can delete only your own data.")

    # User is guaranteed to exist, otherwise they cant authenticate
    users_container.delete_item(
        item=user_id,
        partition_key=user_id,
    )
