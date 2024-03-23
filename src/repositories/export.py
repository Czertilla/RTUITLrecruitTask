from database import Base, new_session
from sqlalchemy import select

class ExportRepo:
    orm = Base

    @classmethod
    def filt(cls, kwargs)-> tuple:
        return tuple(set(kwargs) - set(cls.orm.__annotations__.keys()))

    @classmethod
    async def export(cls, data: list[dict], unique_column_name) -> dict:
        invalid_params = []
        updated_params = []
        count = 0
        badkeys=cls.filt(data[0])
        if badkeys:
            invalid_params.append(f"invalid colums names: {badkeys}, have been ignored")
        for record in data:
            [record.pop(key) for key in badkeys]
            async with new_session() as session:
                model = (
                    await session.execute(
                        select(cls.orm).
                        where(getattr(cls.orm, unique_column_name) == record.get(unique_column_name))
                    )
                ).scalar_one_or_none()
            if model is None:
                model = cls.orm(**record)
                count += 1
                updated = False
            else:
                for key, val in record.items():
                    setattr(model, key, val)
                updated_params.append(str(tuple(record.values())+(model.id,)))
                updated = False
            try:
                async with new_session() as session:
                    await session.merge(model)
                    await session.commit()
            except Exception as e:
                invalid_params.append(f"{e.statement}, ({e.params}) : {e.orig.args[0]}")
                if updated:
                    updated_params.pop(-1)
                else:
                    count -= 1
        return {"added": count, "updated": updated_params, "invalid": invalid_params}

