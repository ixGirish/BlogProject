from fastapi import FastAPI
from Connection import connection
from Router import BlogRouter,UserRouter,login,FileRouter

app = FastAPI()

# Create tables
connection.Base.metadata.create_all(bind=connection.engine)

#Include blog routes
app.include_router(BlogRouter.router)

app.include_router(UserRouter.router)

app.include_router(login.router)

app.include_router(FileRouter.router)