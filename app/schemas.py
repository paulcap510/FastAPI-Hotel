from pydantic import BaseModel, SecretStr, EmailStr
from datetime import datetime
from typing import List, Optional

# RoomType Schema
class RoomTypeBase(BaseModel):
    name: str
    description: Optional[str] = None
    price_per_night: int

class RoomTypeCreate(RoomTypeBase):
    pass

class RoomType(RoomTypeBase):
    id: int
    rooms: List['Room'] = []  

    class Config:
        from_attributes = True 

# Room Schema
class RoomBase(BaseModel):
    room_number: int

class RoomCreate(RoomBase):
    room_type_id: int

class Room(RoomBase):
    id: int
    is_available: bool
    room_type: RoomType  

    class Config:
        from_attributes = True  

# Reservation Schema
class ReservationBase(BaseModel):
    check_in: datetime
    check_out: datetime

class ReservationCreate(ReservationBase):
    user_id: int
    room_id: int

class Reservation(ReservationBase):
    id: int
    user_id: int
    room_id: int
    room: Room  

    class Config:
        from_attributes = True  

# User Schema
class UserBase(BaseModel):
    email: EmailStr  

class UserCreate(UserBase):
    password: SecretStr  

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    reservations: List[Reservation] = []

    class Config:
        from_attributes = True   

class UserRead(UserBase):
    id: int
    is_active: bool
    reservations: List[Reservation] = []  

    class Config:
        from_attributes = True
