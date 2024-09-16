from pydantic import BaseModel, Field

class InfluxQueryRequest(BaseModel):
    equipment_name: str = Field(min_length=4)