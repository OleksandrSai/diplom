from config import settings
from fastapi import FastAPI
import uvicorn
from router import socket_router


app = FastAPI()
app.include_router(router=socket_router, prefix=settings.API_PREFIX)


@app.get("/")
def hello_index():
    return {
        "message": "Hello index!",
    }


if __name__ == "__main__":
    uvicorn.run("app:app", host=settings.HOST, port=settings.PORT, reload=True)
