from database import Base, BaseRepo
from sqlalchemy import select

class ExportRepo(BaseRepo):
    model = Base

    def filt(self, kwargs)-> tuple:
        return tuple(set(kwargs) - set(self.model.__annotations__.keys()))

    async def export(self, data: list[dict], unique_column_name) -> dict:
        invalid_params = []
        updated_params = []
        count = 0
        badkeys=self.filt(data[0])
        if badkeys:
            invalid_params.append(f"invalid colums names: {badkeys}, have been ignored")
        for record in data:
            [record.pop(key) for key in badkeys]
            stmt = (
                select(self.model).
                where(
                    getattr(
                        self.model, 
                        unique_column_name
                    ) 
                    == 
                    record.get(
                        unique_column_name
                    )
                )
            )
            model_data = (await self.execute(stmt)).scalar_one_or_none()
            if model_data is None:
                model_data = self.model(**record)
                count += 1
                updated = False
            else:
                for key, val in record.items():
                    setattr(model_data, key, val)
                updated_params.append(str(tuple(record.values())+(model_data.id,)))
                updated = False
            try:
                await self.merge(model_data)
            except Exception as e:
                invalid_params.append(f"{e.statement}, ({e.params}) : {e.orig.args[0]}")
                if updated:
                    updated_params.pop(-1)
                else:
                    count -= 1
        return {"added": count, "updated": updated_params, "invalid": invalid_params}

