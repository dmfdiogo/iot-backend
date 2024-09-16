from pydantic import BaseModel

class EquipmentResponse(BaseModel):
    id: int
    name: str
    average: int | None = None