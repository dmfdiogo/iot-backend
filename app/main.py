from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware

from .config.config import Config
from .database.pgsql_database import engine, Base
from .routers import auth, user, equipment

app = FastAPI()

origins = [
    Config.FRONTEND_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)

@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(equipment.router)
