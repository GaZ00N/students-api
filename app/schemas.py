from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    """Schema for adding a new student."""

    full_name: str = Field(..., min_length=3, examples=["Иванов Иван Иванович"])
    group: str = Field(..., min_length=2, examples=["ИБ-21"])
    course: int = Field(..., ge=1, le=6, examples=[3])
    average_grade: float = Field(..., ge=0, le=5, examples=[4.6])


class Student(StudentCreate):
    """Schema for a student returned by the API."""

    id: int = Field(..., ge=1, examples=[1])
