import json
from pathlib import Path
from typing import List, Optional

from app.schemas import Student, StudentCreate

DATABASE_PATH = Path(__file__).resolve().parent / "students.json"


def _ensure_database_exists() -> None:
    """Create an empty JSON database if the file was deleted or not copied."""
    if not DATABASE_PATH.exists():
        DATABASE_PATH.write_text("[]", encoding="utf-8")


def _read_students_raw() -> list[dict]:
    _ensure_database_exists()
    with DATABASE_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def _write_students_raw(students: list[dict]) -> None:
    with DATABASE_PATH.open("w", encoding="utf-8") as file:
        json.dump(students, file, ensure_ascii=False, indent=2)


def get_all_students() -> List[Student]:
    return [Student(**student) for student in _read_students_raw()]


def get_student_by_id(student_id: int) -> Optional[Student]:
    for student in _read_students_raw():
        if student.get("id") == student_id:
            return Student(**student)
    return None


def get_students_by_group(group_name: str) -> List[Student]:
    requested_group = group_name.lower()
    return [
        Student(**student)
        for student in _read_students_raw()
        if student.get("group", "").lower() == requested_group
    ]


def add_student(student_data: StudentCreate) -> Student:
    students = _read_students_raw()
    next_id = max((student.get("id", 0) for student in students), default=0) + 1

    new_student = Student(id=next_id, **student_data.model_dump())
    students.append(new_student.model_dump())
    _write_students_raw(students)

    return new_student
