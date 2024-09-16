from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from ..models.user import User
from ..requests.token_request import Token
from ..requests.user_requests import CreateUserRequest
from ..utils.authentication import bcrypt_context, authenticate_user, create_access_token
from ..utils.dependencies import postgres_dependency
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: postgres_dependency,
                      user: CreateUserRequest):

    create_user_model = User(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        hashed_password=bcrypt_context.hash(user.password),
        is_active=True,
        phone_number=user.phone_number
    )

    try:
        db.add(create_user_model)
        db.commit()

        return JSONResponse(content={
            "success": True,
            "message": "User created successfully",
            "user_id": create_user_model.id
        },status_code=201)
    except Exception as e:  # Catch potential database errors
        db.rollback()  # Rollback the transaction if an error occurs
        raise HTTPException(status_code=500, detail=f"Error creating user: {e}")

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: postgres_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))

    return JSONResponse(content={
                "success": True,
                "access_token": token,
                "token_type": "bearer"
            },status_code=201)







