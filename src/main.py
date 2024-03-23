from asyncio import run
from app import app
from utils.dblocalrequests import requests
from repositories import CamerusRepo




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app)
    # run(requests())
    

