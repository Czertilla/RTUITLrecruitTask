from typing import Annotated

from fastapi import Depends
from units_of_work.camera import CameraUOW
from units_of_work.case import CaseUOW
from utils.absract.unit_of_work import ABCUnitOfWork


CameraUOWDep = Annotated[ABCUnitOfWork, Depends(CameraUOW)]
CaseUOWDep = Annotated[ABCUnitOfWork, Depends(CaseUOW)]
