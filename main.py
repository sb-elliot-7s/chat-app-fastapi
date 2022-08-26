from fastapi import FastAPI
from customers.auth.controllers import auth_controllers
from customers.profile.controllers import profile_controllers
import uvicorn
from settings import get_settings

app = FastAPI(title='chat', version='1.0.0')
app.include_router(auth_controllers)
app.include_router(profile_controllers)


def run_server():
    uvicorn.run(
        'main:app',
        host=get_settings().host,
        port=get_settings().port,
        reload=True
    )


if __name__ == '__main__':
    run_server()
