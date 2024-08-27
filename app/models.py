from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime  
from sqlalchemy.orm import relationship 
from .database import Base  


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    reservations = relationship("Reservation", back_populates="user")


class RoomType(Base):
    __tablename__ = "room_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # Name of the room type (e.g., Single, Double, Suite)
    description = Column(String, index=True)  # Description of the room type
    price_per_night = Column(Integer)

    rooms = relationship("Room", back_populates="room_type")


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(Integer, unique=True, index=True)
    is_available = Column(Boolean, default=True)
    room_type_id = Column(Integer, ForeignKey("room_types.id"))

    room_type = relationship("RoomType", back_populates="rooms")
    reservations = relationship("Reservation", back_populates="room")


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    check_in = Column(DateTime)
    check_out = Column(DateTime)

    user = relationship("User", back_populates="reservations")
    room = relationship("Room", back_populates="reservations")
