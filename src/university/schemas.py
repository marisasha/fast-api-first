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


class PostResponse(BaseModel):
    id: int
    message: str
