from fastapi import FastAPI, HTTPException, status

from app.database import add_student, get_all_students, get_student_by_id, get_students_by_group
from app.schemas import Student, StudentCreate

app = FastAPI(
    title="students-api",
    description="Сервис учёта студентов для учебного проекта КубГТУ.",
    version="1.0.0",
)


@app.get("/")
def root() -> dict:
    return {
        "service": "students-api",
        "message": "Сервис учёта студентов работает",
        "docs": "/docs",
    }


@app.get("/students", response_model=list[Student])
def read_students() -> list[Student]:
    return get_all_students()


@app.get("/students/{student_id}", response_model=Student)
def read_student(student_id: int) -> Student:
    student = get_student_by_id(student_id)
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Студент с указанным ID не найден",
        )
    return student


@app.get("/students/group/{group_name}", response_model=list[Student])
def read_students_by_group(group_name: str) -> list[Student]:
    return get_students_by_group(group_name)


@app.post("/students", response_model=Student, status_code=status.HTTP_201_CREATED)
def create_student(student_data: StudentCreate) -> Student:
    return add_student(student_data)
