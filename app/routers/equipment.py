from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from .auth import get_current_user
from ..database.database import SessionLocal
from ..models.equipment import Equipment

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class EquipmentRequest(BaseModel):
    name: str = Field(min_length=3)
    average: int = Field(gt=-1)


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Equipment).all()


@router.get("/equipment/{equipment_id}", status_code=status.HTTP_200_OK)
async def read_equipment(user: user_dependency, db: db_dependency, equipment_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    equipment_model = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if equipment_model is not None:
        return equipment_model
    raise HTTPException(status_code=404, detail='Todo not found.')


@router.post("/equipment", status_code=status.HTTP_201_CREATED)
async def create_equipment(user: user_dependency, db: db_dependency,
                      equipment_request: EquipmentRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    equipment_model = Equipment(**equipment_request.model_dump())

    db.add(equipment_model)
    db.commit()


@router.put("/equipment/{equipment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_equipment(user: user_dependency, db: db_dependency,
                      equipment_request: EquipmentRequest,
                      equipment_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    equipment_model = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if equipment_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')

    equipment_model.name = equipment_request.title
    equipment_model.last_updated = equipment_request.description
    equipment_model.average = equipment_request.priority

    db.add(equipment_model)
    db.commit()


@router.delete("/equipment/{equipment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_equipment(user: user_dependency, db: db_dependency, equipment_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    equipment_model = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if equipment_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    db.query(Equipment).filter(Equipment.id == equipment_id).delete()

    db.commit()












