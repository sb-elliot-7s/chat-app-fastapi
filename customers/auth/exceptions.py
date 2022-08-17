from fastapi import HTTPException, status


class AuthExceptions:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Token expired'
    )

    incorrect_username_or_password = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Incorrect username or password'
    )

    username_exists = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='This username is exists'
    )
