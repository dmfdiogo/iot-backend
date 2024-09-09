from fastapi import FastAPI, Request, status

from .database.database import engine, Base
from .routers import auth, user

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}


app.include_router(auth.router)
app.include_router(user.router)
