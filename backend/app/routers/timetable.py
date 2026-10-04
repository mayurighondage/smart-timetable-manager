from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from ..database import get_db

from ..models import (
    Faculty,
    TimetableEntry
)

from ..schemas import (
    TimetableCreate,
    TimetableOut
)

from ..auth import (
    current_user,
    require_admin
)


router = APIRouter(
    prefix="/timetable",
    tags=["Timetable"]
)


# ==========================================================
# CHECK TIME OVERLAP
# ==========================================================

def time_overlap(
    start1: str,
    end1: str,
    start2: str,
    end2: str
):

    return (
        start1 < end2
        and
        start2 < end1
    )


# ==========================================================
# FORMAT TIMETABLE RESPONSE
# ==========================================================

def timetable_response(
    entry
):

    return {

        "id": entry.id,

        "day": entry.day,

        "start_time": entry.start_time,

        "end_time": entry.end_time,

        "subject": entry.subject,

        "class_name": entry.class_name,

        "room": entry.room,

        "faculty_id": entry.faculty_id,

        "faculty_name": entry.faculty.name,

        "batch": entry.batch,

        "is_lab": entry.is_lab
    }


# ==========================================================
# GET TIMETABLE
# ==========================================================

@router.get(
    "",
    response_model=list[TimetableOut]
)
def get_timetable(

    day: str | None = None,

    class_name: str | None = None,

    search: str | None = None,

    db: Session = Depends(get_db),

    user=Depends(current_user)

):

    query = db.query(
        TimetableEntry
    )

    if day:

        query = query.filter(
            TimetableEntry.day == day
        )

    if class_name:

        query = query.filter(
            TimetableEntry.class_name
            == class_name
        )

    entries = query.all()

    if search:

        search = search.lower()

        entries = [

            entry

            for entry in entries

            if (
                search in entry.subject.lower()
                or
                search in entry.room.lower()
                or
                search in entry.faculty.name.lower()
            )
        ]

    return [
        timetable_response(entry)
        for entry in entries
    ]


# ==========================================================
# GET SINGLE TIMETABLE ENTRY
# ==========================================================

@router.get(
    "/{entry_id}"
)
def get_timetable_entry(

    entry_id: int,

    db: Session = Depends(get_db),

    user=Depends(current_user)

):

    entry = db.get(
        TimetableEntry,
        entry_id
    )

    if not entry:

        raise HTTPException(
            status_code=404,
            detail="Timetable entry not found"
        )

    return timetable_response(
        entry
    )


# ==========================================================
# CREATE TIMETABLE ENTRY
# ADMIN ONLY
# ==========================================================

@router.post(
    "",
    response_model=TimetableOut
)
def create_timetable(

    data: TimetableCreate,

    db: Session = Depends(get_db),

    admin=Depends(require_admin)

):

    faculty = db.get(
        Faculty,
        data.faculty_id
    )

    if not faculty:

        raise HTTPException(
            status_code=404,
            detail="Faculty not found"
        )

    existing = db.query(
        TimetableEntry
    ).filter(
        TimetableEntry.day == data.day
    ).all()

    conflicts = []

    for entry in existing:

        if not time_overlap(
            data.start_time,
            data.end_time,
            entry.start_time,
            entry.end_time
        ):

            continue

        if entry.faculty_id == data.faculty_id:

            conflicts.append(
                "Faculty is already scheduled"
            )

        if entry.room == data.room:

            conflicts.append(
                "Room is already occupied"
            )

        if entry.class_name == data.class_name:

            conflicts.append(
                "Class already has another lecture"
            )

    if conflicts:

        raise HTTPException(

            status_code=409,

            detail={
                "message":
                    "Timetable conflict detected",

                "conflicts":
                    list(set(conflicts))
            }
        )

    timetable = TimetableEntry(

        day=data.day,

        start_time=data.start_time,

        end_time=data.end_time,

        subject=data.subject,

        class_name=data.class_name,

        room=data.room,

        faculty_id=data.faculty_id,

        batch=data.batch,

        is_lab=data.is_lab
    )

    db.add(timetable)

    db.commit()

    db.refresh(timetable)

    return timetable_response(
        timetable
    )


# ==========================================================
# DELETE TIMETABLE ENTRY
# ADMIN ONLY
# ==========================================================

@router.delete(
    "/{entry_id}"
)
def delete_timetable(

    entry_id: int,

    db: Session = Depends(get_db),

    admin=Depends(require_admin)

):

    entry = db.get(
        TimetableEntry,
        entry_id
    )

    if not entry:

        raise HTTPException(
            status_code=404,
            detail="Timetable entry not found"
        )

    db.delete(entry)

    db.commit()

    return {

        "message":
            "Timetable entry deleted successfully",

        "entry_id":
            entry_id
    }


# ==========================================================
# CLASH DETECTOR
# ==========================================================

@router.get(
    "/clashes/check"
)
def detect_clashes(

    db: Session = Depends(get_db),

    user=Depends(current_user)

):

    entries = db.query(
        TimetableEntry
    ).all()

    clashes = []

    for i in range(
        len(entries)
    ):

        first = entries[i]

        for j in range(
            i + 1,
            len(entries)
        ):

            second = entries[j]

            if first.day != second.day:

                continue

            if not time_overlap(
                first.start_time,
                first.end_time,
                second.start_time,
                second.end_time
            ):

                continue

            if first.faculty_id == second.faculty_id:

                clashes.append({

                    "type": "Faculty",

                    "message":
                        f"{first.faculty.name} "
                        f"has overlapping classes",

                    "entry_1": first.id,

                    "entry_2": second.id
                })

            if first.room == second.room:

                clashes.append({

                    "type": "Room",

                    "message":
                        f"{first.room} is double-booked",

                    "entry_1": first.id,

                    "entry_2": second.id
                })

            if first.class_name == second.class_name:

                clashes.append({

                    "type": "Class",

                    "message":
                        f"{first.class_name} "
                        f"has overlapping classes",

                    "entry_1": first.id,

                    "entry_2": second.id
                })

    return {

        "total_clashes":
            len(clashes),

        "status":
            "PASS"
            if len(clashes) == 0
            else "CONFLICT",

        "clashes":
            clashes
    }