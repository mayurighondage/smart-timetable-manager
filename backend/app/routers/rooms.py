from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Room, TimetableEntry
from ..auth import current_user


router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)


# ==========================================================
# ROOM OCCUPANCY
# ==========================================================

@router.get("/occupancy")
def room_occupancy(
    day: str,
    start_time: str,
    end_time: str,
    db: Session = Depends(get_db),
    user=Depends(current_user)
):

    rooms = db.query(Room).filter(
        Room.active == True
    ).all()

    occupied_rooms = []
    available_rooms = []

    for room in rooms:

        entries = db.query(TimetableEntry).filter(
            TimetableEntry.room == room.name,
            TimetableEntry.day == day
        ).all()

        occupied = False

        for entry in entries:

            if (
                start_time < entry.end_time
                and entry.start_time < end_time
            ):
                occupied = True
                break

        if occupied:
            occupied_rooms.append({
                "room_id": room.id,
                "room_name": room.name,
                "room_type": room.room_type,
                "capacity": room.capacity,
                "status": "Occupied"
            })

        else:
            available_rooms.append({
                "room_id": room.id,
                "room_name": room.name,
                "room_type": room.room_type,
                "capacity": room.capacity,
                "status": "Available"
            })

    return {
        "day": day,
        "start_time": start_time,
        "end_time": end_time,
        "occupied_rooms": occupied_rooms,
        "available_rooms": available_rooms
    }