from pydantic import BaseModel


# ==========================================================
# LOGIN
# ==========================================================

class LoginRequest(BaseModel):

    email: str
    password: str


class TokenResponse(BaseModel):

    access_token: str
    token_type: str = "bearer"


# ==========================================================
# FACULTY
# ==========================================================

class FacultyCreate(BaseModel):

    name: str

    email: str

    password: str

    role: str = "faculty"

    expertise: list[str] = []

    max_hours: int = 16


class FacultyOut(BaseModel):

    id: int

    name: str

    email: str

    role: str

    expertise: list[str]

    max_hours: int

    current_hours: int


# ==========================================================
# TIMETABLE
# ==========================================================

class TimetableCreate(BaseModel):

    day: str

    start_time: str

    end_time: str

    subject: str

    class_name: str

    room: str

    faculty_id: int

    batch: str | None = None

    is_lab: bool = False


class TimetableOut(BaseModel):

    id: int

    day: str

    start_time: str

    end_time: str

    subject: str

    class_name: str

    room: str

    faculty_id: int

    faculty_name: str

    batch: str | None

    is_lab: bool