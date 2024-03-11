from app import app

from database.repositories import CamerusRepo
from asyncio import run
from schemas.dynamic import DynamicModels
from uuid import uuid4
from datetime import datetime

async def db_requests():
    # await CamerusRepo.create_root("camerus1")

    # await CamerusRepo.put("camerus1", "transport_chars", "str", field_attrs={
    #     "pattern": "[A-Z]{3}"
    # })
    # await CamerusRepo.put("camerus1", "transport_numbers", "str", field_attrs={
    #     "pattern": "[0-9]{3}"
    # })
    # await CamerusRepo.put("camerus1", "transport_region", "str", field_attrs={
    #     "pattern": "[0-9]{2}"
    # })
    # await CamerusRepo.put("camerus1", "camera_id", "UUID")
    # await CamerusRepo.put("camerus1", "violation_id", "UUID")
    # await CamerusRepo.put("camerus1", "violation_value", "str")
    # await CamerusRepo.put("camerus1", "skill_value", "int", field_attrs={
    #     "ge": 1,
    #     "le": 100
    # })
    # await CamerusRepo.put("camerus1", "datetime", "datetime")

    # await CamerusRepo.create_root("camerus2")
    # await CamerusRepo.put("camerus2", "transport", "dict")
    # await CamerusRepo.put("camerus2.transport", "chars", "str", field_attrs={
    #     "pattern": "[A-Z]{3}"
    # })
    # await CamerusRepo.put("camerus2.transport", "numbers", "str", field_attrs={
    #     "pattern": "[0-9]{3}"
    # })
    # await CamerusRepo.put("camerus2.transport", "region", "str", field_attrs={
    #     "pattern": "[0-9]{2}"
    # })
    # await CamerusRepo.put("camerus2", "camera", "dict")
    # await CamerusRepo.put("camerus2.camera", "id", "UUID")
    # await CamerusRepo.put("camerus2", "violation", "dict")
    # await CamerusRepo.put("camerus2.violation", "id", "UUID")
    # await CamerusRepo.put("camerus2.violation", "value", "str", field_attrs={
    #     "max_length": 64
    # })
    # await CamerusRepo.put("camerus2", "skill", "dict")
    # await CamerusRepo.put("camerus2.skill", "value", "int", field_attrs={
    #     "ge": 1,
    #     "le": 100
    # })
    # await CamerusRepo.put("camerus2", "datetime", "dict")
    # await CamerusRepo.put("camerus2.datetime", "year", "int", field_attrs={
    #     "ge": 1970
    # })
    # await CamerusRepo.put("camerus2.datetime", "month", "int", field_attrs={
    #     "ge": 1,
    #     "le": 12
    # })
    # await CamerusRepo.put("camerus2.datetime", "day", "int", field_attrs={
    #     "ge": 1,
    #     "le": 31
    # })
    # await CamerusRepo.put("camerus2.datetime", "hour", "int", field_attrs={
    #     "ge": 0,
    #     "le": 23
    # })
    # await CamerusRepo.put("camerus2.datetime", "minute", "int", field_attrs={
    #     "ge": 0,
    #     "le": 59
    # })
    # await CamerusRepo.put("camerus2.datetime", "seconds", "int", field_attrs={
    #     "ge": 0,
    #     "le": 59
    # })
    await CamerusRepo.put("camerus2.datetime", "utc_offset", "str", field_attrs={
        "pattern": "[+][0-9]{2}:[0-9]{2}"
    })
    ...

if __name__ == "__main__":
    run(db_requests())
    

