from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Faculty, TimetableEntry, Subject
from ..auth import current_user


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


# ==========================================================
# 1. FACULTY WORKLOAD ANALYTICS
# ==========================================================

@router.get("/workload")
def workload_analytics(
    db: Session = Depends(get_db),
    user: Faculty = Depends(current_user)
):

    faculty_list = db.query(Faculty).filter(
        Faculty.department == user.department,
        Faculty.active == True
    ).all()

    analytics = []

    for faculty in faculty_list:

        current_hours = db.query(TimetableEntry).filter(
            TimetableEntry.faculty_id == faculty.id
        ).count()

        max_hours = faculty.max_hours

        remaining_hours = max(
            max_hours - current_hours,
            0
        )

        if current_hours >= max_hours:
            workload_status = "Full"

        elif current_hours >= max_hours * 0.75:
            workload_status = "High"

        elif current_hours >= max_hours * 0.50:
            workload_status = "Medium"

        else:
            workload_status = "Low"

        analytics.append({
            "faculty_id": faculty.id,
            "faculty_name": faculty.name,
            "current_hours": current_hours,
            "max_hours": max_hours,
            "remaining_hours": remaining_hours,
            "workload_status": workload_status
        })

    return {
        "department": user.department,
        "faculty_workload": analytics
    }


# ==========================================================
# 2. SYLLABUS PROGRESS
# ==========================================================

@router.get("/syllabus")
def syllabus_progress(
    db: Session = Depends(get_db),
    user: Faculty = Depends(current_user)
):

    subjects = db.query(Subject).filter(
        Subject.faculty_id == user.id
    ).all()

    progress = []

    for subject in subjects:

        total_units = subject.total_units
        completed_units = subject.completed_units

        if total_units > 0:
            percentage = (
                completed_units / total_units
            ) * 100
        else:
            percentage = 0

        progress.append({
            "subject_id": subject.id,
            "subject": subject.name,
            "class_name": subject.class_name,
            "total_units": total_units,
            "completed_units": completed_units,
            "remaining_units": max(
                total_units - completed_units,
                0
            ),
            "progress_percentage": round(
                percentage,
                2
            )
        })

    return {
        "faculty": user.name,
        "department": user.department,
        "subjects": progress
    }


# ==========================================================
# 3. DASHBOARD STATISTICS
# ==========================================================

@router.get("/dashboard")
def dashboard_statistics(
    db: Session = Depends(get_db),
    user: Faculty = Depends(current_user)
):

    faculty_count = db.query(Faculty).filter(
        Faculty.department == user.department,
        Faculty.active == True
    ).count()

    timetable_count = db.query(TimetableEntry).filter(
        TimetableEntry.faculty_id == user.id
    ).count()

    subject_count = db.query(Subject).filter(
        Subject.faculty_id == user.id
    ).count()

    total_units = 0
    completed_units = 0

    subjects = db.query(Subject).filter(
        Subject.faculty_id == user.id
    ).all()

    for subject in subjects:
        total_units += subject.total_units
        completed_units += subject.completed_units

    if total_units > 0:
        syllabus_percentage = (
            completed_units / total_units
        ) * 100
    else:
        syllabus_percentage = 0

    remaining_units = max(
        total_units - completed_units,
        0
    )

    return {
        "faculty": user.name,
        "department": user.department,
        "faculty_count": faculty_count,
        "assigned_classes": timetable_count,
        "subjects": subject_count,
        "total_syllabus_units": total_units,
        "completed_syllabus_units": completed_units,
        "remaining_syllabus_units": remaining_units,
        "syllabus_progress_percentage": round(
            syllabus_percentage,
            2
        )
    }