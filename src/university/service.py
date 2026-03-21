from fastapi import APIRouter, FastAPI, HTTPException
from fastapi import status
from sqlalchemy import select


from src.university.dependencies import SessionDep
from src.university.models import *
from src.university.schemas import *


router = APIRouter(tags=["university"])


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


# @router.get(
#     "/books",
#     summary="See all books",
#     description="See all user's books ",
#     status_code=status.HTTP_200_OK,
# )
# async def see_books(session: SessionDep) -> list[BookGetSchema]:

#     result = await session.execute(select(BookModel))
#     books = result.scalars().all()
#     return books


# @router.get(
#     "/books/{id}",
#     summary="See all books",
#     description="See all user's books ",
#     status_code=status.HTTP_200_OK,
# )
# async def see_book(session: SessionDep, id: int) -> BookGetSchema:
#     result = await session.execute(select(BookModel).where(BookModel.id == id))
#     book = result.scalar_one_or_none()
#     if not book:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not found"
#         )
#     return book
