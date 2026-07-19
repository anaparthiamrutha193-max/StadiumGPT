from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/")
def auth_home():
    return {"message": "Authentication API"}


@router.post("/register")
def register():
    return {
        "success": True,
        "message": "User registered successfully"
    }


@router.post("/login")
def login():
    return {
        "success": True,
        "message": "Login successful"
    }