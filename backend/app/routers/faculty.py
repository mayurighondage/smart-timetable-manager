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
    FacultyCreate,
    FacultyOut
)

from ..security import hash_password

from ..auth import (
    current_user,
    require_admin
)


router = APIRouter(
    prefix="/faculty",
    tags=["Faculty"]
)


# ==========================================================
# CALCULATE CURRENT HOURS
# ==========================================================

def calculate_hours(
    db: Session,
    faculty_id: int
):

    return db.query(
        TimetableEntry
    ).filter(
        TimetableEntry.faculty_id == faculty_id
    ).count()


# ==========================================================
# FORMAT FACULTY RESPONSE
# ==========================================================

def faculty_response(
    faculty,
    db: Session
):

    return {

        "id": faculty.id,

        "name": faculty.name,

        "email": faculty.email,

        "role": faculty.role,

        "expertise": [
            x.strip()
            for x in faculty.expertise.split(",")
            if x.strip()
        ],

        "max_hours": faculty.max_hours,

        "current_hours": calculate_hours(
            db,
            faculty.id
        )
    }


# ==========================================================
# GET ALL FACULTY
# ==========================================================

@router.get(
    "",
    response_model=list[FacultyOut]
)
def get_all_faculty(

    db: Session = Depends(get_db),

    user=Depends(current_user)

):

    faculty = db.query(
        Faculty
    ).filter(
        Faculty.active == True
    ).all()

    return [
        faculty_response(
            f,
            db
        )
        for f in faculty
    ]


# ==========================================================
# GET SINGLE FACULTY
# ==========================================================

@router.get(
    "/{faculty_id}",
    response_model=FacultyOut
)
def get_faculty(

    faculty_id: int,

    db: Session = Depends(get_db),

    user=Depends(current_user)

):

    faculty = db.get(
        Faculty,
        faculty_id
    )

    if not faculty:

        raise HTTPException(
            status_code=404,
            detail="Faculty not found"
        )

    return faculty_response(
        faculty,
        db
    )


# ==========================================================
# CREATE FACULTY
# ADMIN ONLY
# ==========================================================

@router.post(
    "",
    response_model=FacultyOut
)
def create_faculty(

    data: FacultyCreate,

    db: Session = Depends(get_db),

    admin=Depends(require_admin)

):

    existing = db.query(
        Faculty
    ).filter(
        Faculty.email == data.email
    ).first()

    if existing:

        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    faculty = Faculty(

        name=data.name,

        email=data.email,

        password_hash=hash_password(
            data.password
        ),

        role=data.role,

        expertise=",".join(
            data.expertise
        ),

        max_hours=data.max_hours,

        active=True
    )

    db.add(faculty)

    db.commit()

    db.refresh(faculty)

    return faculty_response(
        faculty,
        db
    )


# ==========================================================
# UPDATE FACULTY
# ADMIN ONLY
# ==========================================================

@router.put(
    "/{faculty_id}"
)
def update_faculty(

    faculty_id: int,

    data: FacultyCreate,

    db: Session = Depends(get_db),

    admin=Depends(require_admin)

):

    faculty = db.get(
        Faculty,
        faculty_id
    )

    if not faculty:

        raise HTTPException(
            status_code=404,
            detail="Faculty not found"
        )

    faculty.name = data.name

    faculty.email = data.email

    faculty.role = data.role

    faculty.expertise = ",".join(
        data.expertise
    )

    faculty.max_hours = data.max_hours

    if data.password:

        faculty.password_hash = hash_password(
            data.password
        )

    db.commit()

    db.refresh(faculty)

    return faculty_response(
        faculty,
        db
    )


# ==========================================================
# DEACTIVATE FACULTY
# ADMIN ONLY
# ==========================================================

@router.delete(
    "/{faculty_id}"
)
def delete_faculty(

    faculty_id: int,

    db: Session = Depends(get_db),

    admin=Depends(require_admin)

):

    faculty = db.get(
        Faculty,
        faculty_id
    )

    if not faculty:

        raise HTTPException(
            status_code=404,
            detail="Faculty not found"
        )

    faculty.active = False

    db.commit()

    return {

        "message":
            "Faculty deactivated successfully",

        "faculty_id":
            faculty_id
    }