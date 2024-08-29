from fastapi import FastAPI
from .database import engine
from .models import Base 
from .middleware import cors
from .routers import users, rooms
from .middleware import cors

app = FastAPI()

cors.add_cors_middleware(app)

app.include_router(users.router)  
app.include_router(rooms.router, prefix="/rooms") 

@app.get("/")
def read_root():
    return {"message": "Welcome to the Hotel Booking API"}
