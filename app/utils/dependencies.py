from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.pgsql_database import SessionLocal
from app.database.influx_database import InfluxDB
from app.utils.authentication import get_current_user


def get_postgres_session():
    postgres_db = SessionLocal()
    try:
        yield postgres_db
    finally:
        postgres_db.close()

def get_influxdb():
    influx_db = InfluxDB()
    try:
        yield influx_db
    finally:
        influx_db.close()

postgres_dependency = Annotated[Session, Depends(get_postgres_session)]
user_dependency = Annotated[dict, Depends(get_current_user)]
influx_dependency = Annotated[InfluxDB, Depends(get_influxdb)]