import datetime

from pydantic import BaseModel


class StudentSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    birth_date: datetime.datetime
    enrollment_date: datetime.datetime


class StudentGetSchema(StudentSchema):
    id: int


class CoursesSchema(BaseModel):
    name: str
    description: str
    credits: int
    created_at: datetime.datetime


class CoursesGetSchema(CoursesSchema):
    id: int


class StudentCoursesSchema(BaseModel):
    student_id: int
    course_id: int
    grade: float
    enrollment_date: datetime.datetime


class StudentCoursesGetSchema(StudentCoursesSchema):
    id: int


class PostResponse(BaseModel):
    id: int
    message: str
