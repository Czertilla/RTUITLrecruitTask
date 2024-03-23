import json
from typing import Annotated
from uuid import UUID
from datetime import datetime
from pydantic import create_model, BaseModel, ValidationError, Field
from database.repositories import CamerusRepo
from typing import Type
from models import DependenciesOrm


class DynamicModels:
    extraTypes = {
    "UUID": UUID,
    "datetime": datetime,
    }
    extraTypes.update(__builtins__)

    camerus_list: list[Type[BaseModel]] = []
    camerus_pattern_list: list[str]

    @classmethod
    def get_builtin(cls, name: str):
        return cls.extraTypes.get(name)
    
    @classmethod
    async def create(cls, name: str, data: list[DependenciesOrm]):
        kwargs = {}
        for dependency in data:
            val_type = cls.get_builtin(dependency.value_type)
            field_attrs = {
                "validate_default": True
            }
            if val_type is dict:
                val_type = await cls.create(dependency.key, await CamerusRepo.construct(dependency.id))
            field_attrs.update(dependency.field_attrs)
            kwargs.update({dependency.key: (Annotated[val_type, Field(**field_attrs)], None)})
        setattr(cls, name, new_model:=create_model(name, __base__=BaseModel, **kwargs))
        return new_model

    @classmethod
    async def generate(cls):
        root_list = await CamerusRepo.collect()
        for root in root_list:
            cls.camerus_list.append(await cls.create(
                (await CamerusRepo.find_by_id(root)).key, 
                await CamerusRepo.construct(root)
                ))
        await cls.set_pattern()
            
    @classmethod
    async def set_pattern(cls) -> None:
        cls.camerus_pattern_list = [cam_type.__name__ for cam_type in cls.camerus_list]

    @classmethod
    async def validate(cls, data:dict) -> Type[BaseModel] | dict[str, ValidationError]:
        exceptions: dict[str, ValidationError] = {}
        for camerus in cls.camerus_list:
            try:
                model = camerus.model_validate_json(json.dumps(data))
                return model, camerus.__name__
            except ValidationError as e:
                exceptions.update({camerus.__name__: e.errors()})
        else:
            return exceptions, "error"
