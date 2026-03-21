import datetime
import time
from typing import Optional

from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class CourseModel(Base):
    __tablename__ = "course"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    credits: Mapped[int]
    created_at: Mapped[datetime.datetime]

    students: Mapped[list["StudentCourseModel"]] = relationship(back_populates="course")


class StudentModel(Base):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]
    birth_date: Mapped[datetime.datetime]
    enrollment_date: Mapped[datetime.datetime]

    courses: Mapped[list["StudentCourseModel"]] = relationship(back_populates="student")


class StudentCourseModel(Base):
    __tablename__ = "student_course"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(
        ForeignKey("student.id", ondelete="CASCADE")
    )
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id", ondelete="CASCADE"))
    grade: Mapped[Optional[float]] = mapped_column(
        CheckConstraint("grade >= 1 AND grade <= 5", name="check_grade_range"),
        nullable=True,
    )
    enrollment_date: Mapped[datetime.datetime]
    __table_args__ = (
        UniqueConstraint("student_id", "course_id", name="uq_student_course"),
    )
    student: Mapped["StudentModel"] = relationship(back_populates="courses")
    course: Mapped["CourseModel"] = relationship(back_populates="students")
    enrollment_date: Mapped[datetime.datetime]
