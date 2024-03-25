from asyncio import run

from units_of_work.all import AllUOW

async def requests():
    uow = AllUOW()
    async with uow:
#   fill with Repo classmethods
        # await uow.camerus.create_root("camerus1")

        # await uow.camerus.put("camerus1", "transport_chars", "str", field_attrs={
        #     "pattern": "[A-Z]{3}"
        # })
        # await uow.camerus.put("camerus1", "transport_numbers", "str", field_attrs={
        #     "pattern": "[0-9]{3}"
        # })
        # await uow.camerus.put("camerus1", "transport_region", "str", field_attrs={
        #     "pattern": "[0-9]{2}"
        # })
        # await uow.camerus.put("camerus1", "camera_id", "UUID")
        # await uow.camerus.put("camerus1", "violation_id", "UUID")
        # await uow.camerus.put("camerus1", "violation_value", "str")
        # await uow.camerus.put("camerus1", "skill_value", "int", field_attrs={
        #     "ge": 1,
        #     "le": 100
        # })
        # await uow.camerus.put("camerus1", "datetime", "datetime")

        # await uow.camerus.create_root("camerus2")
        # await uow.camerus.put("camerus2", "transport", "dict")
        # await uow.camerus.put("camerus2.transport", "chars", "str", field_attrs={
        #     "pattern": "[A-Z]{3}"
        # })
        # await uow.camerus.put("camerus2.transport", "numbers", "str", field_attrs={
        #     "pattern": "[0-9]{3}"
        # })
        # await uow.camerus.put("camerus2.transport", "region", "str", field_attrs={
        #     "pattern": "[0-9]{2}"
        # })
        # await uow.camerus.put("camerus2", "camera", "dict")
        # await uow.camerus.put("camerus2.camera", "id", "UUID")
        # await uow.camerus.put("camerus2", "violation", "dict")
        # await uow.camerus.put("camerus2.violation", "id", "UUID")
        # await uow.camerus.put("camerus2.violation", "value", "str", field_attrs={
        #     "max_length": 64
        # })
        # await uow.camerus.put("camerus2", "skill", "dict")
        # await uow.camerus.put("camerus2.skill", "value", "int", field_attrs={
        #     "ge": 1,
        #     "le": 100
        # })
        # await uow.camerus.put("camerus2", "datetime", "dict")
        # await uow.camerus.put("camerus2.datetime", "year", "int", field_attrs={
        #     "ge": 1970
        # })
        # await uow.camerus.put("camerus2.datetime", "month", "int", field_attrs={
        #     "ge": 1,
        #     "le": 12
        # })
        # await uow.camerus.put("camerus2.datetime", "day", "int", field_attrs={
        #     "ge": 1,
        #     "le": 31
        # })
        # await uow.camerus.put("camerus2.datetime", "hour", "int", field_attrs={
        #     "ge": 0,
        #     "le": 23
        # })
        # await uow.camerus.put("camerus2.datetime", "minute", "int", field_attrs={
        #     "ge": 0,
        #     "le": 59
        # })
        # await uow.camerus.put("camerus2.datetime", "seconds", "int", field_attrs={
        #     "ge": 0,
        #     "le": 59
        # })
        # await uow.camerus.put("camerus2.datetime", "utc_offset", "str", field_attrs={
        #     "pattern": "[+][0-9]{2}:[0-9]{2}"
        # })
        # await uow.camerus.create_root("camerus3")
        # await uow.camerus.put("camerus3", "transport", "str", field_attrs={
        #     "pattern": "[0-9][A-Z]{3}[0-9]{4}"
        # })
        # await uow.camerus.put("camerus3", "camera", "dict")
        # await uow.camerus.put("camerus3.camera", "id", "UUID")
        # await uow.camerus.put("camerus3", "violation", "dict")
        # await uow.camerus.put("camerus3.violation", "id", "UUID")
        # await uow.camerus.put("camerus3.violation", "value", "str", field_attrs={
        #     "max_length": 64})
        # await uow.camerus.put("camerus3", "skill", "int", field_attrs={
        #     "ge": 1,
        #     "le": 100
        # })
        # await uow.camerus.put("camerus3", "datetime", "int")
        # await uow.users.set_manager("5f382e1c-d335-48d4-a4c9-66217a538bcc")
        await uow.commit()  

if __name__ == "__main__":
    run(requests())