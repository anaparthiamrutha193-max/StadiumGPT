from fastapi import APIRouter

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.get("/")
def get_chat():
    return {
        "message": "Welcome to StadiumGPT AI Chat"
    }


@router.post("/")
def send_chat():
    return {
        "response": "AI Response Generated Successfully"
    }