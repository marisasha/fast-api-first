from fastapi import APIRouter

from src.university.service import router as books_router


main_router = APIRouter()

main_router.include_router(books_router)
