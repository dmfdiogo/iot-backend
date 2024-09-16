from typing import List

from fastapi import APIRouter, HTTPException, Path, UploadFile, File
from fastapi.responses import JSONResponse
import csv
import io
from starlette import status
from ..config.config import Config
from ..models.equipment import Equipment
from fastapi.params import Query
from datetime import datetime
from influxdb_client import Point, WritePrecision

from ..requests.equipment_requests import EquipmentRequest
from ..responses.equipment_responses import EquipmentResponse
from ..utils.dependencies import user_dependency, postgres_dependency, influx_dependency

router = APIRouter(
    prefix='/equipment',
    tags=['equipment']
)

@router.get("/", response_model=List[EquipmentResponse])
async def read_all(user: user_dependency, postgres_db: postgres_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    equipment_data = postgres_db.query(Equipment).all()
    return equipment_data
    # return JSONResponse(content={
    #     "success": True,
    #     "equipments":
    # },status_code=200)


@router.get("/{equipment_id}", status_code=status.HTTP_200_OK)
async def read_equipment(user: user_dependency, postgres_db: postgres_dependency, equipment_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    equipment_model = postgres_db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if equipment_model is not None:
        return equipment_model
    raise HTTPException(status_code=404, detail='Todo not found.')

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_equipment(user: user_dependency, postgres_db: postgres_dependency,
                           equipment_request: EquipmentRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    equipment_model = Equipment(**equipment_request.model_dump())

    postgres_db.add(equipment_model)
    postgres_db.commit()


@router.put("/{equipment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_equipment(user: user_dependency, postgres_db: postgres_dependency,
                           equipment_request: EquipmentRequest,
                           equipment_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    equipment_model = postgres_db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if equipment_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')

    equipment_model.name = equipment_request.title
    equipment_model.last_updated = equipment_request.description
    equipment_model.average = equipment_request.priority

    postgres_db.add(equipment_model)
    postgres_db.commit()


@router.delete("/{equipment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_equipment(user: user_dependency, postgres_db: postgres_dependency, equipment_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    equipment_model = postgres_db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if equipment_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    postgres_db.query(Equipment).filter(Equipment.id == equipment_id).delete()

    postgres_db.commit()

@router.get("/sensor/get_data")
async def get_sensor_data_by_equipment_name(user: user_dependency,
                                            influxdb: influx_dependency,
                                            equipment_name: str = Query(default=None, description="Equipment name (ex: EQ-124500)"),
                                            start_time: str | None = Query(default=None, description="Time period for the query (Ex: -24h)")):

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    influx_query = f"""
            from(bucket: "{Config.INFLUXDB_BUCKET}")
              |> range(start: {start_time or "-24h"})
              |> filter(fn: (r) => r["_measurement"] == "{Config.INFLUX_MEASUREMENT}")
              |> filter(fn: (r) => r["equipmentId"] == "{equipment_name.upper()}")
            """
    try:
        tables = influxdb.query_data(influx_query)
        results = []
        for table in tables:
            for record in table.records:
                results.append(
                    {
                        "time": record.get_time(),
                        "measurement": record.get_measurement(),
                        "field": record.get_field(),
                        "value": record.get_value(),
                    }
                )
        return {"results": results}
    except Exception as e:
        return {"error": str(e)}

@router.post("/upload_csv/")
async def upload_csv(user: user_dependency, influxdb: influx_dependency, postgres_db: postgres_dependency, file: UploadFile = File(...)):
        if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed')

        contents = await file.read()
        csv_reader = csv.DictReader(io.StringIO(contents.decode("utf-8")))

        file_data = []
        for row in csv_reader:
            file_data.append(row)

        for record in file_data:
            timestamp_str = record['timestamp']
            timestamp_dt = datetime.fromisoformat(timestamp_str)

            timestamp_ns = int(timestamp_dt.timestamp() * 1e9)

            point = Point(Config.INFLUX_MEASUREMENT).tag("equipmentId", record['equipmentId'].upper()).field("value", float(record['value'])).time(timestamp_ns, WritePrecision.NS)
            try:
                influxdb.write_data(point)

                equipment_name = record['equipmentId'].upper()
                existing_equipment = postgres_db.query(Equipment).filter_by(name=equipment_name).first()
                if not existing_equipment:
                    new_equipment = Equipment(name=equipment_name)
                    postgres_db.add(new_equipment)
                    postgres_db.commit()

            except Exception as e:
                postgres_db.rollback()
                print(f"Error writing to InfluxDB: {e}")

        return JSONResponse(content={"message": "CSV uploaded and inserted into InfluxDB successfully"}, status_code=200)









