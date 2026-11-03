from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
import httpx

from .schemas import OrderCreate
from .config import settings
from .auth import CurrentUser, get_current_user
from .routers.router import router

app = FastAPI()

app.include_router(router)
