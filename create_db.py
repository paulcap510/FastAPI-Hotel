from app.database import Base, engine
from app.models import User, RoomType, Room, Reservation  # Import all your models

Base.metadata.create_all(bind=engine)
