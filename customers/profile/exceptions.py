from fastapi import HTTPException, status


class ProfileExceptions:
    username_exists = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='User with this username exists'
    )