from typing import Annotated

from fastapi import Depends
from units_of_work.camera import CameraUOW
from units_of_work.case import CaseUOW
from units_of_work.export import ExportUOW
from units_of_work.user import UserUOW
from utils.absract.unit_of_work import ABCUnitOfWork


CameraUOWDep = Annotated[ABCUnitOfWork, Depends(CameraUOW)]
CaseUOWDep = Annotated[ABCUnitOfWork, Depends(CaseUOW)]
ExportUOWDep = Annotated[ABCUnitOfWork, Depends(ExportUOW)]
UserUOWDep = Annotated[ABCUnitOfWork, Depends(UserUOW)]