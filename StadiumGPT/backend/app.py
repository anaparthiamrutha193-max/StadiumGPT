import logging
from contextlib import asynccontextmanager
from datetime import UTC, datetime, timedelta
from typing import Annotated
from uuid import uuid4

import jwt
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from google import genai
from google.genai import types
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.database import Base, engine, get_db
from database.models import Chat, Notification, User
from utils.security import settings

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger('stadiumgpt')
pwd = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth = OAuth2PasswordBearer(tokenUrl='/auth/login')
Db = Annotated[Session, Depends(get_db)]

class Register(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
class UserUpdate(BaseModel): full_name: str | None = Field(default=None, min_length=2, max_length=120)
class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; full_name: str; email: EmailStr; created_at: datetime
class Token(BaseModel): access_token: str; token_type: str = 'bearer'
class ChatIn(BaseModel): message: str = Field(min_length=1, max_length=4000)
class ChatOut(BaseModel): id: int; response: str; created_at: datetime
class NavigationOut(BaseModel): route: str; distance: str; estimated_time: str
class CrowdOut(BaseModel): zone: str; density: str; percentage: int = Field(ge=0, le=100)
class WeatherOut(BaseModel): temperature: int; condition: str; humidity: int; rain_probability: int
class EmergencyIn(BaseModel): type: str = Field(min_length=2, max_length=80); location: str = Field(min_length=2, max_length=160)
class EmergencyOut(BaseModel): status: str; incident_id: str; reported_at: datetime
class TranslationIn(BaseModel): text: str = Field(min_length=1, max_length=4000); language: str = Field(min_length=2, max_length=80)
class TranslationOut(BaseModel): translated_text: str; language: str
class NotificationOut(BaseModel): id: int; title: str; description: str; type: str; created_at: datetime


def current_user(token: Annotated[str, Depends(oauth)], db: Db) -> User:
    err = HTTPException(401, 'Could not validate credentials', headers={'WWW-Authenticate': 'Bearer'})
    try:
        subject = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]).get('sub')
        if not subject: raise err
        user = db.get(User, int(subject))
        if not user: raise err
        return user
    except (InvalidTokenError, ValueError) as exc: raise err from exc
CurrentUser = Annotated[User, Depends(current_user)]

def make_token(user: User) -> str:
    return jwt.encode({'sub': str(user.id), 'exp': datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)}, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

def gemini(prompt: str) -> str:
    if not settings.gemini_api_key: raise HTTPException(503, 'Gemini is not configured. Set GEMINI_API_KEY in .env.')
    try:
        response = genai.Client(api_key=settings.gemini_api_key).models.generate_content(model=settings.gemini_model, contents=prompt, config=types.GenerateContentConfig(temperature=0.3))
        if not response.text or not response.text.strip(): raise RuntimeError('Empty Gemini response')
        return response.text.strip()
    except HTTPException: raise
    except Exception as exc:
        logger.exception('Gemini request failed')
        raise HTTPException(503, 'The AI assistant is temporarily unavailable.') from exc

@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    logger.info('Database initialized')
    yield
app = FastAPI(title=settings.app_name, version='1.0.0', description='AI-powered smart stadium assistant API for FIFA World Cup 2026.', lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
@app.exception_handler(Exception)
async def unexpected(request: Request, exc: Exception):
    logger.exception('Unhandled request error: %s', request.url.path)
    return JSONResponse(status_code=500, content={'detail':'An unexpected server error occurred'})
@app.get('/', tags=['Health'])
def root(): return {'message':'Welcome to StadiumGPT API', 'docs':'/docs'}
@app.get('/health', tags=['Health'])
def health(): return {'status':'healthy', 'environment':settings.environment}
@app.post('/auth/register', response_model=UserOut, status_code=201, tags=['Authentication'])
def register(payload: Register, db: Db):
    email = payload.email.lower()
    if db.scalar(select(User).where(User.email == email)): raise HTTPException(409, 'An account with this email already exists')
    user = User(full_name=payload.full_name.strip(), email=email, password_hash=pwd.hash(payload.password))
    db.add(user); db.commit(); db.refresh(user); return user
@app.post('/auth/login', response_model=Token, tags=['Authentication'])
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], db: Db):
    user = db.scalar(select(User).where(User.email == form.username.lower()))
    if not user or not pwd.verify(form.password, user.password_hash): raise HTTPException(401, 'Incorrect email or password', headers={'WWW-Authenticate':'Bearer'})
    return Token(access_token=make_token(user))
@app.get('/auth/me', response_model=UserOut, tags=['Authentication'])
def me(user: CurrentUser): return user
@app.post('/chat', response_model=ChatOut, tags=['AI Assistant'])
def chat(payload: ChatIn, user: CurrentUser, db: Db):
    response = gemini('You are StadiumGPT, a concise and safety-conscious FIFA World Cup 2026 stadium assistant. Do not invent live facts; advise official staff/signage where needed. Fan question: ' + payload.message.strip())
    item=Chat(user_id=user.id, message=payload.message.strip(), response=response); db.add(item); db.commit(); db.refresh(item); return ChatOut(id=item.id,response=item.response,created_at=item.created_at)
@app.get('/chat/history', tags=['AI Assistant'])
def chat_history(user: CurrentUser, db: Db): return db.scalars(select(Chat).where(Chat.user_id==user.id).order_by(Chat.created_at.desc()).limit(50)).all()
@app.get('/navigation', response_model=NavigationOut, tags=['Stadium Operations'])
def navigation(destination: str | None=Query(None,max_length=160), origin: str | None=Query(None,max_length=160)):
    return NavigationOut(route=f'{origin or "Your current location"} ? Main Concourse ? {destination or "Gate A"}', distance='350m', estimated_time='5 min')
@app.get('/crowd', response_model=CrowdOut, tags=['Stadium Operations'])
def crowd(zone: str | None=Query(None,max_length=160)):
    selected=zone or 'Gate A'; percentage=sum(map(ord,selected))%61+25
    return CrowdOut(zone=selected,density='High' if percentage>=75 else 'Moderate' if percentage>=45 else 'Low',percentage=percentage)
@app.get('/weather', response_model=WeatherOut, tags=['Stadium Operations'])
def weather(): return WeatherOut(temperature=31,condition='Sunny',humidity=58,rain_probability=10)
@app.post('/emergency', response_model=EmergencyOut, status_code=202, tags=['Safety'])
def emergency(payload: EmergencyIn, _: CurrentUser): return EmergencyOut(status='Emergency Team Dispatched',incident_id='EMG-'+uuid4().hex[:8].upper(),reported_at=datetime.now(UTC))
@app.post('/translation', response_model=TranslationOut, tags=['AI Assistant'])
def translation(payload: TranslationIn, _: CurrentUser): return TranslationOut(translated_text=gemini(f'Translate into {payload.language}. Return only the translation. Text: {payload.text}'),language=payload.language)
@app.get('/notifications', response_model=list[NotificationOut], tags=['Notifications'])
def notifications(user: CurrentUser, db: Db):
    items=db.scalars(select(Notification).where(Notification.user_id==user.id).order_by(Notification.created_at.desc())).all()
    if not items:
        item=Notification(user_id=user.id,title='Match Starts in 30 Minutes',description='Please make your way to your seating section.',notification_type='info'); db.add(item); db.commit(); db.refresh(item); items=[item]
    return [NotificationOut(id=x.id,title=x.title,description=x.description,type=x.notification_type,created_at=x.created_at) for x in items]
@app.get('/profile', response_model=UserOut, tags=['Profile'])
def profile(user: CurrentUser): return user
@app.put('/profile', response_model=UserOut, tags=['Profile'])
def update_profile(payload: UserUpdate, user: CurrentUser, db: Db):
    if payload.full_name is not None: user.full_name=payload.full_name.strip(); db.commit(); db.refresh(user)
    return user