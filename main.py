from fastapi import FastAPI
from customers.auth.controllers import auth_controllers

app = FastAPI(title='chat', version='1.0.0')
app.include_router(auth_controllers)
