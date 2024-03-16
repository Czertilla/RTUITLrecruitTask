
from io import BytesIO
from pandas import DataFrame, read_excel
from numpy import nan

def import_excel(data: bytes) -> list[dict]:
    frame = read_excel(BytesIO(data))
    frame.replace(nan, None, inplace=True)
    return frame.to_dict("records")
