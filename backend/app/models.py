from datetime import datetime

from sqlalchemy import (
    String,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    Text
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from .database import Base


# ==========================================================
# FACULTY TABLE
# ==========================================================

class Faculty(Base):

    __tablename__ = "faculty"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash: Mapped[str] = mapped_column(
        String(300),
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(30),
        default="faculty"
    )

    expertise: Mapped[str] = mapped_column(
        Text,
        default=""
    )

    max_hours: Mapped[int] = mapped_column(
        Integer,
        default=16
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    timetable = relationship(
        "TimetableEntry",
        back_populates="faculty",
        cascade="all, delete-orphan"
    )


# ==========================================================
# TIMETABLE TABLE
# ==========================================================

class TimetableEntry(Base):

    __tablename__ = "timetable"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    day: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    start_time: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    end_time: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    subject: Mapped[str] = mapped_column(
        String(120),
        nullable=False
    )

    class_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    room: Mapped[str] = mapped_column(
        String(80),
        nullable=False
    )

    faculty_id: Mapped[int] = mapped_column(
        ForeignKey("faculty.id"),
        nullable=False
    )

    batch: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    is_lab: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    faculty = relationship(
        "Faculty",
        back_populates="timetable"
    )


# ==========================================================
# SUBJECT TABLE
# ==========================================================

class Subject(Base):

    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(120),
        unique=True,
        nullable=False
    )

    class_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    total_units: Mapped[int] = mapped_column(
        Integer,
        default=6
    )

    completed_units: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    faculty_id: Mapped[int | None] = mapped_column(
        ForeignKey("faculty.id"),
        nullable=True
    )


# ==========================================================
# ROOM TABLE
# ==========================================================

class Room(Base):

    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(80),
        unique=True,
        nullable=False
    )

    room_type: Mapped[str] = mapped_column(
        String(30),
        default="Classroom"
    )

    capacity: Mapped[int] = mapped_column(
        Integer,
        default=60
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )


# ==========================================================
# SUBSTITUTE REQUEST
# ==========================================================

class SubstituteRequest(Base):

    __tablename__ = "substitute_requests"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    requester_id: Mapped[int] = mapped_column(
        ForeignKey("faculty.id")
    )

    recommended_id: Mapped[int] = mapped_column(
        ForeignKey("faculty.id")
    )

    subject: Mapped[str] = mapped_column(
        String(120)
    )

    class_name: Mapped[str] = mapped_column(
        String(100),
        default=""
    )

    day: Mapped[str] = mapped_column(
        String(20),
        default=""
    )

    slot: Mapped[str] = mapped_column(
        String(50)
    )

    reason: Mapped[str] = mapped_column(
        Text,
        default=""
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="Pending"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )