from fastapi import FastAPI
from routers.user import router as user_route
from routers.transaction import router as transaction_route

app = FastAPI()

app.include_router(user_route)
app.include_router(transaction_route)
