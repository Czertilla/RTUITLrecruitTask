
from io import BytesIO
from pandas import DataFrame, read_excel


def import_excel(data: bytes) -> list[dict]:
    frame = read_excel(BytesIO(data))
    return frame.to_dict("records")
