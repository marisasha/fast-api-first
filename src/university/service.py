from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi import status
from sqlalchemy import func, select
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
async def see_students(request: Request, session: SessionDep):

    result = await session.execute(select(StudentModel))
    students = result.scalars().all()

    return templates.TemplateResponse(
        "Students.html", {"request": request, "students": students}
    )


@router.get(
    "/courses",
    summary="See all courses",
    description="See all courses",
    status_code=status.HTTP_200_OK,
)
async def see_course(request: Request, session: SessionDep):

    result = await session.execute(select(CourseModel))
    courses = result.scalars().all()

    return templates.TemplateResponse(
        "Courses.html", {"request": request, "courses": courses}
    )


@router.get(
    "/enrollments",
    summary="See all enrollments",
    description="See all enrollments",
    status_code=status.HTTP_200_OK,
)
async def see_enrollments(request: Request, session: SessionDep):

    result = await session.execute(
        select(StudentCourseModel).options(
            selectinload(StudentCourseModel.student),
            selectinload(StudentCourseModel.course),
        )
    )
    enrollments = result.scalars().all()

    return templates.TemplateResponse(
        "Enrollments.html", {"request": request, "enrollments": enrollments}
    )


@router.get(
    "/olap/roll-up/course",
    summary="See OLAP Roll-up ",
    description="See OLAP Roll-up by courses",
    status_code=status.HTTP_200_OK,
)
async def see_roll_up_by_courses(request: Request, session: SessionDep):

    result = await session.execute(
        select(
            CourseModel.name,
            func.count().label("enrollment_count"),
            func.min(StudentCourseModel.grade).label("min_grade"),
            func.max(StudentCourseModel.grade).label("max_grade"),
            func.avg(StudentCourseModel.grade).label("avg_grade"),
        )
        .join(StudentCourseModel, StudentCourseModel.course_id == CourseModel.id)
        .group_by(CourseModel.name)
    )

    roll_up_course = [
        {
            "course_name": row.name,
            "enrollment_count": row.enrollment_count,
            "min_grade": float(row.min_grade) if row.min_grade else None,
            "max_grade": float(row.max_grade) if row.max_grade else None,
            "avg_grade": float(row.avg_grade) if row.avg_grade else None,
        }
        for row in result
    ]

    return templates.TemplateResponse(
        "RollUpCourse.html", {"request": request, "roll_up_course": roll_up_course}
    )


@router.get(
    "/olap/roll-up/student",
    summary="See OLAP Roll-up ",
    description="See OLAP Roll-up by students",
    status_code=status.HTTP_200_OK,
)
async def see_roll_up_by_students(request: Request, session: SessionDep):

    result = await session.execute(
        select(
            StudentModel.first_name,
            StudentModel.last_name,
            func.count().label("enrollment_count"),
            func.min(StudentCourseModel.grade).label("min_grade"),
            func.max(StudentCourseModel.grade).label("max_grade"),
            func.avg(StudentCourseModel.grade).label("avg_grade"),
        )
        .join(StudentCourseModel, StudentCourseModel.student_id == StudentModel.id)
        .group_by(StudentModel.first_name, StudentModel.last_name)
    )

    roll_up_student = [
        {
            "student_first_name": row.first_name,
            "student_last_name": row.last_name,
            "enrollment_count": row.enrollment_count,
            "min_grade": float(row.min_grade) if row.min_grade else None,
            "max_grade": float(row.max_grade) if row.max_grade else None,
            "avg_grade": float(row.avg_grade) if row.avg_grade else None,
        }
        for row in result
    ]

    return templates.TemplateResponse(
        "RollUpStudent.html", {"request": request, "roll_up_student": roll_up_student}
    )


@router.get(
    "/olap/slice/course/{id}",
    summary="See OLAP Slice ",
    description="See OLAP Slice by course id ",
    status_code=status.HTTP_200_OK,
)
async def see_slice_by_students(request: Request, session: SessionDep, id: int = 1):

    result = await session.execute(
        select(
            CourseModel.name,
            StudentModel.first_name,
            StudentModel.last_name,
            StudentCourseModel.grade,
        )
        .join(StudentCourseModel, StudentCourseModel.course_id == CourseModel.id)
        .join(StudentModel, StudentModel.id == StudentCourseModel.student_id)
        .where(CourseModel.id == id)
    )

    slice_by_course = [
        {
            "course_name": row.name,
            "student_first_name": row.first_name,
            "student_last_name": row.last_name,
            "grade": row.grade,
        }
        for row in result
    ]

    all_course_result = await session.execute(select(CourseModel))

    return templates.TemplateResponse(
        "SliceCourse.html",
        {
            "request": request,
            "slice_by_course": slice_by_course,
            "all_course": all_course_result.scalars().all(),
        },
    )


@router.get(
    "/olap/slice/student/{id}",
    summary="See OLAP Slice by Student",
    description="See OLAP Slice by student id - список курсов и оценок студента",
    status_code=status.HTTP_200_OK,
)
async def see_slice_by_student(request: Request, session: SessionDep, id: int = 1):

    result = await session.execute(
        select(
            StudentModel.first_name,
            StudentModel.last_name,
            CourseModel.name.label("course_name"),
            StudentCourseModel.grade,
        )
        .join(StudentCourseModel, StudentCourseModel.student_id == StudentModel.id)
        .join(CourseModel, CourseModel.id == StudentCourseModel.course_id)
        .where(StudentModel.id == id)
        .order_by(CourseModel.name)
    )

    slice_by_student = [
        {
            "student_first_name": row.first_name,
            "student_last_name": row.last_name,
            "course_name": row.course_name,
            "grade": float(row.grade) if row.grade else None,
        }
        for row in result
    ]
    all_students_result = await session.execute(
        select(
            StudentModel.id, StudentModel.first_name, StudentModel.last_name
        ).order_by(StudentModel.last_name, StudentModel.first_name)
    )
    return templates.TemplateResponse(
        "SliceStudent.html",
        {
            "request": request,
            "slice_by_student": slice_by_student,
            "all_students": all_students_result.all(),
        },
    )


@router.get(
    "/olap/fact-table",
    summary="See OLAP Fact Table",
    description="See OLAP Fact Table - все пары курс-студент с оценками и датами",
    status_code=status.HTTP_200_OK,
)
async def see_fact_table(request: Request, session: SessionDep):

    result = await session.execute(
        select(
            CourseModel.name.label("course_name"),
            StudentModel.first_name.label("student_first_name"),
            StudentModel.last_name.label("student_last_name"),
            StudentCourseModel.grade,
            StudentCourseModel.enrollment_date.label("enrollment_date"),
        )
        .join(StudentCourseModel, StudentCourseModel.course_id == CourseModel.id)
        .join(StudentModel, StudentModel.id == StudentCourseModel.student_id)
        .order_by(CourseModel.name, StudentModel.last_name)
    )

    fact_table_data = [
        {
            "course_name": row.course_name,
            "student_first_name": row.student_first_name,
            "student_last_name": row.student_last_name,
            "grade": float(row.grade) if row.grade else None,
            "enrollment_date": (
                row.enrollment_date.strftime("%d.%m.%Y %H:%M")
                if row.enrollment_date
                else None
            ),
        }
        for row in result
    ]

    return templates.TemplateResponse(
        "FactTable.html",
        {
            "request": request,
            "fact_table_data": fact_table_data,
        },
    )
