from fastapi import APIRouter, HTTPException, Path
from starlette import status
from passlib.context import CryptContext
from ..models.user import User
from ..requests.user_requests import UserVerification
from ..utils.dependencies import user_dependency, postgres_dependency

router = APIRouter(
    prefix='/user',
    tags=['user']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: postgres_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(User).filter(User.id == user.get('id')).first()


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: postgres_dependency,
                          user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(User).filter(User.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()


@router.put("/phonenumber/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def change_phonenumber(user: user_dependency, db: postgres_dependency,
                          phone_number: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(User).filter(User.id == user.get('id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()






