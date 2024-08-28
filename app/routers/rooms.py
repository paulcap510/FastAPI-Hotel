from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import RoomType as RoomTypeModel, Room as RoomModel
from ..schemas import RoomTypeCreate, RoomType, RoomCreate, Room

router = APIRouter()

@router.post("/room-types/", response_model=RoomType)
def create_room_type(room_type: RoomTypeCreate, db: Session = Depends(get_db)):
    db_room_type = RoomTypeModel(  
        name=room_type.name,
        description=room_type.description,
        price_per_night=room_type.price_per_night
    )
    db.add(db_room_type)
    db.commit()
    db.refresh(db_room_type)
    return db_room_type

@router.get("/room-types/", response_model=List[RoomType])
def get_room_types(db: Session = Depends(get_db)):
    return db.query(RoomTypeModel).all()

@router.post("/rooms/", response_model=Room)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    db_room = RoomModel(**room.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

@router.get("/rooms/", response_model=List[Room])
def get_rooms(db: Session = Depends(get_db)):
    return db.query(RoomModel).all()
