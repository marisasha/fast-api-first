from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi import status
from sqlalchemy import select
from sqlalchemy.orm import selectinload


from src.university.dependencies import SessionDep
from src.university.models import *
from src.university.schemas import *

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


router = APIRouter(tags=["university"])
templates = Jinja2Templates(directory="templates")


@router.post(
    "/students",
    summary="Create a new student",
    description="Creates a new student and returns ID",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_student(
    student: StudentSchema,
    session: SessionDep,
) -> PostResponse:
    new_student = StudentModel(
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email,
        birth_date=student.birth_date,
        enrollment_date=student.enrollment_date,
    )
    session.add(new_student)
    await session.commit()
    await session.refresh(new_student)

    return PostResponse(
        id=new_student.id,
        message=f"Student '{new_student.first_name}' successfully created !",
    )


@router.get(
    "/students/{id}",
    summary="See student",
    description="See student for id",
    status_code=status.HTTP_200_OK,
)
async def see_book(session: SessionDep, id: int) -> StudentGetSchema:
    result = await session.execute(select(StudentModel).where(StudentModel.id == id))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {id} not found",
        )
    return book


@router.get(
    "/students",
    summary="See all students",
    description="See all students",
    status_code=status.HTTP_200_OK,
)
async def see_books(request: Request, session: SessionDep) -> list[StudentGetSchema]:

    result = await session.execute(select(StudentModel))
    students = result.scalars().all()

    return templates.TemplateResponse(
        "students.html", {"request": request, "students": students}
    )


@router.get(
    "/courses",
    summary="See all courses",
    description="See all courses",
    status_code=status.HTTP_200_OK,
)
async def see_books(request: Request, session: SessionDep) -> list[CoursesGetSchema]:

    result = await session.execute(select(CourseModel))
    courses = result.scalars().all()

    return templates.TemplateResponse(
        "courses.html", {"request": request, "courses": courses}
    )


@router.get(
    "/enrollments",
    summary="See all enrollments",
    description="See all enrollments",
    status_code=status.HTTP_200_OK,
)
async def see_books(
    request: Request, session: SessionDep
) -> list[StudentCoursesGetSchema]:

    result = await session.execute(
        select(StudentCourseModel).options(
            selectinload(StudentCourseModel.student),
            selectinload(StudentCourseModel.course),
        )
    )
    enrollments = result.scalars().all()

    return templates.TemplateResponse(
        "enrollments.html", {"request": request, "enrollments": enrollments}
    )
