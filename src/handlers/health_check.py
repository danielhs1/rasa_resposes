from fastapi import APIRouter

router = APIRouter()


@router.get("/health/", tags=["health"])
async def user_message():
    return {"status": "Ok"}
