from fastapi import APIRouter

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.get("/")
def get_notifications():
    return [
        {
            "title": "Match Reminder",
            "description": "Your match starts in 30 minutes"
        }
    ]