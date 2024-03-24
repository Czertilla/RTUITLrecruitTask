from sqlalchemy import select, exists

from database import BaseRepo
from models.cameras import CameraOrm
from uuid import UUID
import logging
from utils.exceptor import Exceptor

logger = logging.getLogger(__name__)
exc = Exceptor()

class CameraRepo(BaseRepo):
    model = CameraOrm
