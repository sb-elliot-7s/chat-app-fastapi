from fastapi import FastAPI
from customers.auth.controllers import auth_controllers
from customers.profile.controllers import profile_controllers

app = FastAPI(title='chat', version='1.0.0')
app.include_router(auth_controllers)
app.include_router(profile_controllers)
