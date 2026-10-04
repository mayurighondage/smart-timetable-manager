from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Faculty, TimetableEntry, SubstituteRequest
from ..auth import current_user


router = APIRouter(
    prefix="/substitutes",
    tags=["Substitutes"]
)


# ==========================================================
# TIME OVERLAP CHECK
# ==========================================================

def time_overlap(
    start1: str,
    end1: str,
    start2: str,
    end2: str
):
    return start1 < end2 and start2 < end1


# ==========================================================
# FACULTY AVAILABILITY CHECK
# ==========================================================

def is_faculty_available(
    db: Session,
    faculty_id: int,
    day: str,
    start_time: str,
    end_time: str
):

    entries = db.query(TimetableEntry).filter(
        TimetableEntry.faculty_id == faculty_id,
        TimetableEntry.day == day
    ).all()

    for entry in entries:

        if time_overlap(
            start_time,
            end_time,
            entry.start_time,
            entry.end_time
        ):
            return False

    return True


# ==========================================================
# WORKLOAD
# ==========================================================

def get_workload(
    db: Session,
    faculty_id: int
):

    return db.query(TimetableEntry).filter(
        TimetableEntry.faculty_id == faculty_id
    ).count()


# ==========================================================
# AI SUBSTITUTE RECOMMENDATION
# ==========================================================

@router.get("/recommend")
def recommend_substitute(
    timetable_id: int,
    db: Session = Depends(get_db),
    user: Faculty = Depends(current_user)
):

    timetable = db.query(TimetableEntry).filter(
        TimetableEntry.id == timetable_id
    ).first()

    if not timetable:
        raise HTTPException(
            status_code=404,
            detail="Timetable entry not found"
        )

    absent_faculty = db.query(Faculty).filter(
        Faculty.id == timetable.faculty_id
    ).first()

    if not absent_faculty:
        raise HTTPException(
            status_code=404,
            detail="Faculty not found"
        )

    class_entries = db.query(TimetableEntry).filter(
        TimetableEntry.class_name == timetable.class_name
    ).all()

    class_faculty_ids = {
        entry.faculty_id
        for entry in class_entries
    }

    candidates = db.query(Faculty).filter(
        Faculty.department == absent_faculty.department,
        Faculty.active == True
    ).all()

    recommendations = []

    for faculty in candidates:

        if faculty.id == absent_faculty.id:
            continue

        if faculty.id not in class_faculty_ids:
            continue

        if not is_faculty_available(
            db,
            faculty.id,
            timetable.day,
            timetable.start_time,
            timetable.end_time
        ):
            continue

        recommendations.sort(
    key=lambda x: x["current_workload"]
)

        if workload >= faculty.max_hours:
            continue

        recommendations.append({
            "faculty_id": faculty.id,
            "faculty_name": faculty.name,
            "department": faculty.department,
            "current_workload": workload,
            "max_hours": faculty.max_hours,
            "available": True,
            "class_name": timetable.class_name,
            "subject": timetable.subject,
            "day": timetable.day,
            "start_time": timetable.start_time,
            "end_time": timetable.end_time
        })

    recommendations.sort(
        key=lambda x: x["current_workload"]
    )

    return {
        "message": "Substitute recommendations generated",
        "absent_faculty": absent_faculty.name,
        "department": absent_faculty.department,
        "subject": timetable.subject,
        "class_name": timetable.class_name,
        "day": timetable.day,
        "start_time": timetable.start_time,
        "end_time": timetable.end_time,
        "recommendations": recommendations
    }


# ==========================================================
# FACULTY AVAILABILITY
# ==========================================================

@router.get("/availability")
def check_faculty_availability(
    day: str,
    start_time: str,
    end_time: str,
    db: Session = Depends(get_db),
    user: Faculty = Depends(current_user)
):

    faculty_list = db.query(Faculty).filter(
        Faculty.department == user.department,
        Faculty.active == True
    ).all()

    available_faculty = []

    for faculty in faculty_list:

        if is_faculty_available(
            db,
            faculty.id,
            day,
            start_time,
            end_time
        ):
            available_faculty.append({
                "faculty_id": faculty.id,
                "faculty_name": faculty.name,
                "department": faculty.department,
                "available": True
            })

    return {
        "day": day,
        "start_time": start_time,
        "end_time": end_time,
        "available_faculty": available_faculty
    }

# ==========================================================
# CREATE SUBSTITUTE REQUEST
# ==========================================================

@router.post("/request")
def create_substitute_request(
    timetable_id: int,
    recommended_id: int,
    reason: str = "",
    db: Session = Depends(get_db),
    user: Faculty = Depends(current_user)
):

    timetable = db.query(TimetableEntry).filter(
        TimetableEntry.id == timetable_id
    ).first()

    if not timetable:
        raise HTTPException(
            status_code=404,
            detail="Timetable entry not found"
        )

    recommended = db.query(Faculty).filter(
        Faculty.id == recommended_id,
        Faculty.active == True
    ).first()

    if not recommended:
        raise HTTPException(
            status_code=404,
            detail="Recommended faculty not found"
        )

    request = SubstituteRequest(
        requester_id=user.id,
        recommended_id=recommended_id,
        subject=timetable.subject,
        class_name=timetable.class_name,
        day=timetable.day,
        slot=f"{timetable.start_time}-{timetable.end_time}",
        reason=reason,
        status="Pending"
    )

    db.add(request)
    db.commit()
    db.refresh(request)

    return {
        "message": "Substitute request created successfully",
        "request_id": request.id,
        "requester": user.name,
        "recommended_faculty": recommended.name,
        "status": request.status
    }
# ==========================================================
# ACCEPT / REJECT SUBSTITUTE REQUEST
# ==========================================================

@router.put("/request/{request_id}")
def update_substitute_request(
    request_id: int,
    status: str,
    db: Session = Depends(get_db),
    user: Faculty = Depends(current_user)
):

    if status not in ["Accepted", "Rejected"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be Accepted or Rejected"
        )

    request = db.query(SubstituteRequest).filter(
        SubstituteRequest.id == request_id
    ).first()

    if not request:
        raise HTTPException(
            status_code=404,
            detail="Substitute request not found"
        )

    if request.recommended_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="Only the recommended faculty can respond"
        )

    if request.status != "Pending":
        raise HTTPException(
            status_code=400,
            detail="Request has already been processed"
        )

    request.status = status

    db.commit()
    db.refresh(request)

    return {
        "message": f"Substitute request {status.lower()}",
        "request_id": request.id,
        "status": request.status,
        "faculty": user.name
    }