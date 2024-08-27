from fastapi import FastAPI
from .database import engine
from .models import Base 
from .middleware import cors
from .routers import users 

app = FastAPI()
app.include_router(users.router)  

@app.get("/")
def read_root():
    return {"message": "Welcome to the Hotel Booking API"}
