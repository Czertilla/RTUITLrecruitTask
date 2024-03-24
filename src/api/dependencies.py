from fastapi import FastAPI

from repositories.cameras import CameraRepo
from repositories.cases import CaseRepo
from repositories.files import FileRepo
from repositories.users import UserRepo
from services.cameras import CameraService
from services.cases import CaseService
from services.files import FileService
from services.users import Userservice
from utils.abstract_serv import BaseService
from .routers import routers
from .auth.routers import include_routers as include_auth_routers


def include_routers(app: FastAPI) -> None:
    for router in routers:
        app.include_router(router)
    include_auth_routers(app)


def get_camera_service():
    return CameraService(CameraRepo)


def get_case_service():
    return CaseService(CaseRepo)


def get_file_service():
    return FileService(FileRepo)


def get_user_service():
    return Userservice(UserRepo)