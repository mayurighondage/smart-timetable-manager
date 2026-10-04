from .models import (
    Faculty,
    Subject,
    TimetableEntry,
    Room
)

from .security import hash_password


# ==========================================================
# DEMO FACULTY
# ==========================================================

FACULTY = [

    (
        "Admin",
        "admin@edunova.local",
        "admin",
        ["Administration"],
        16,
        "admin123"
    ),

    (
        "Dr. Sharma",
        "sharma@edunova.local",
        "faculty",
        ["Machine Learning", "Advanced AI"],
        16,
        "faculty123"
    ),

    (
        "Prof. Patil",
        "patil@edunova.local",
        "faculty",
        ["DBMS", "Python", "SQL"],
        16,
        "faculty123"
    ),

    (
        "Prof. Joshi",
        "joshi@edunova.local",
        "faculty",
        ["DBMS", "Python", "SQL"],
        16,
        "faculty123"
    ),

    (
        "Dr. Kulkarni",
        "kulkarni@edunova.local",
        "faculty",
        [
            "Machine Learning",
            "AI",
            "Data Structures"
        ],
        16,
        "faculty123"
    ),

    (
        "Prof. Pawar",
        "pawar@edunova.local",
        "faculty",
        [
            "Computer Networks",
            "DBMS"
        ],
        16,
        "faculty123"
    )
]


def seed_database(db):

    # Don't create duplicate data
    if db.query(Faculty).count() > 0:
        return


    faculty_map = {}


    # ======================================================
    # CREATE FACULTY
    # ======================================================

    for (
        name,
        email,
        role,
        expertise,
        max_hours,
        password
    ) in FACULTY:

        faculty = Faculty(

            name=name,

            email=email,

            role=role,

            expertise=",".join(expertise),

            max_hours=max_hours,

            password_hash=hash_password(password),

            active=True
        )

        db.add(faculty)

        db.flush()

        faculty_map[name] = faculty


    # ======================================================
    # SUBJECTS
    # ======================================================

    subjects = [

        (
            "Machine Learning",
            "TY AI&DS",
            6,
            4,
            "Dr. Sharma"
        ),

        (
            "Advanced AI Topics",
            "B.Tech AI&DS",
            6,
            5,
            "Dr. Sharma"
        ),

        (
            "DBMS",
            "SY AI&DS",
            6,
            5,
            "Prof. Patil"
        ),

        (
            "Python Programming",
            "FY AI&DS",
            6,
            3,
            "Prof. Joshi"
        ),

        (
            "Data Structures",
            "SY AI&DS",
            6,
            2,
            "Dr. Kulkarni"
        ),

        (
            "Computer Networks",
            "SY AI&DS",
            6,
            2,
            "Prof. Pawar"
        )
    ]


    for (
        name,
        class_name,
        total,
        completed,
        faculty_name
    ) in subjects:

        subject = Subject(

            name=name,

            class_name=class_name,

            total_units=total,

            completed_units=completed,

            faculty_id=faculty_map[faculty_name].id
        )

        db.add(subject)


    # ======================================================
    # ROOMS
    # ======================================================

    rooms = [

        ("Room 101", "Classroom", 60),

        ("Room 102", "Classroom", 60),

        ("Room 103", "Classroom", 60),

        ("Room 104", "Classroom", 60),

        ("Lab 201", "AI Lab", 40),

        ("Lab 202", "DS Lab", 40)
    ]


    for (
        name,
        room_type,
        capacity
    ) in rooms:

        db.add(
            Room(

                name=name,

                room_type=room_type,

                capacity=capacity
            )
        )


    # ======================================================
    # TIMETABLE
    # ======================================================

    timetable = [

        (
            "Monday",
            "09:00",
            "10:00",
            "Machine Learning",
            "TY AI&DS",
            "Room 101",
            "Dr. Sharma"
        ),

        (
            "Monday",
            "10:00",
            "11:00",
            "DBMS",
            "SY AI&DS",
            "Room 102",
            "Prof. Patil"
        ),

        (
            "Monday",
            "11:15",
            "12:15",
            "Data Structures",
            "SY AI&DS",
            "Room 101",
            "Dr. Kulkarni"
        ),

        (
            "Monday",
            "12:15",
            "13:15",
            "AI & Robotics",
            "B.Tech AI&DS",
            "Lab 202",
            "Prof. Joshi"
        ),

        (
            "Tuesday",
            "09:00",
            "10:00",
            "DBMS",
            "SY AI&DS",
            "Room 102",
            "Prof. Patil"
        ),

        (
            "Tuesday",
            "11:15",
            "12:15",
            "Computer Networks",
            "SY AI&DS",
            "Room 201",
            "Prof. Pawar"
        ),

        (
            "Tuesday",
            "14:00",
            "15:00",
            "Advanced AI Topics",
            "B.Tech AI&DS",
            "Room 102",
            "Dr. Sharma"
        ),

        (
            "Wednesday",
            "09:00",
            "10:00",
            "Python Programming",
            "FY AI&DS",
            "Room 103",
            "Prof. Joshi"
        )
    ]


    for row in timetable:

        (
            day,
            start,
            end,
            subject,
            class_name,
            room,
            faculty_name
        ) = row

        db.add(

            TimetableEntry(

                day=day,

                start_time=start,

                end_time=end,

                subject=subject,

                class_name=class_name,

                room=room,

                faculty_id=faculty_map[faculty_name].id
            )
        )


    db.commit()