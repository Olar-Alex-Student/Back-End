"""
Author: Vizitiu Valentin Iulian
License: CC0 “No Rights Reserved”
Link: https://creativecommons.org/publicdomain/zero/1.0/

You are free to copy, modify and use the code in any way. I am not responsible for what you use it for.
"""

from fastapi import APIRouter, HTTPException, Body, Depends, Path, status

from .models import User, UserInDatabase, UpdatedUser
from .functions import get_user_by_email_or_name
from ..database.cosmo_db import users_container
from ..authentication.oath2 import get_current_user, get_password_hash

router = APIRouter(
    prefix="/api/v1/users"
)


@router.post(path="/",
             tags=["users"],
             description="Create a new user.")
async def create_new_user(
        new_user: UserInDatabase = Body(title="A JSON with the initial user data. All fields are "
                                              "mandatory, except fiscal code, only companies should have this.")
) -> User:
    # Anyone can create a new user.
    # In a real application, they will need to verify their email and solve a captcha

    if len(new_user.name) < 3:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Account name must be at least 3 characters long.")

    # Cannot set fiscal code for individual accounts
    if new_user.fiscal_code and new_user.account_type == 'individual':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot set 'fiscal code' for individuals.")

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

    # No need to create a UUID, since the account name is unique
    # But cosmo DB NoSQL required all items to have an id key
    # I could store the name inside id, and then change id to name before sending the response, to avoid duplicate data
    # But I like it more this way for this "small" project, since it's not really a production app
    new_item = {'id': new_user.name,
                **new_user.dict(),
                'password': get_password_hash(new_user.password)}

    users_container.create_item(new_item)

    return new_user


@router.get(path="/{user_id}",
            tags=["users"],
            description="Get all of the user's data")
async def get_current_user(
        user_id: str = Path(example="Vizitiu Valentin",
                            description="The email or name of the user."),
        current_user: User = Depends(get_current_user)
) -> User:

    if user_id != current_user.email and user_id != current_user.name:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only get the current user's data.")

    return current_user


@router.put(path="/{user_id}",
            tags=["users"],
            description="Update any of the user fields.\n"
                        "In the body give only the values you wish to update.\n"
                        "⚠ You cannot update the user's account name.\n")
async def update_user(
        updated_user: UpdatedUser,
        current_user: UserInDatabase = Depends(get_current_user),
        user_id: str = Path(example="Vizitiu Valentin",
                            description="The email or name of the user."),
) -> UpdatedUser:
    # Removes the empty fields from the received updated user
    clean_updated_user = {k: v for k, v in updated_user.dict().items() if v}

    if 'password' in clean_updated_user:
        clean_updated_user['password'] = get_password_hash(clean_updated_user['password'])

    for key in current_user.dict():
        if key not in clean_updated_user:
            clean_updated_user[key] = getattr(current_user, key)

    # Creates the updated user, and puts the non-updated fields to have the same value as the current data
    updated_user = UpdatedUser(
        **clean_updated_user
    )

    if user_id != current_user.email and user_id != current_user.name:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only get the current user's data.")

    # Cannot change account type
    if updated_user.account_type and current_user.account_type != updated_user.account_type:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="'account type' field cannot be updated.")

    # Cannot set fiscal code for individual accounts
    if updated_user.fiscal_code and current_user.account_type == 'individual':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot set 'fiscal code' for individuals.")

    # Cannot update account name
    if updated_user.name and updated_user.name != current_user.name:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="'account name' field cannot be updated.")

    updated_email = updated_user.email != current_user.email

    # If they modified the email or account name, check if one already exists
    if updated_email:
        user = get_user_by_email_or_name(account_name=updated_user.name,
                                         email=updated_user.email)

        if user:
            detail = f"User with the email '{updated_user.email}' already exists."
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)

    # We can create the updated user
    new_user = {'id': current_user.name,
                'password': get_password_hash(updated_user.password),
                **updated_user.dict()}

    # Now we can save the updated data
    users_container.upsert_item(new_user)

    return updated_user


@router.delete(path="/{user_id}",
               tags=["users"],
               description="Delete your account.")
async def delete_user(
        user_id: str = Path(example="Vizitiu Valentin",
                            description="The email or name of the user."),
        current_user: UserInDatabase = Depends(get_current_user)
) -> None:

    if user_id != current_user.email and user_id != current_user.name:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only get the current user's data.")

    # User is guaranteed to exist, otherwise they cant authenticate
    users_container.delete_item(
        item=current_user.name,
        partition_key=current_user.name,
    )
