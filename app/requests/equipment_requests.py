from pydantic import BaseModel, Field

class EquipmentRequest(BaseModel):
    name: str = Field(min_length=3)
    average: int = Field(gt=-1)