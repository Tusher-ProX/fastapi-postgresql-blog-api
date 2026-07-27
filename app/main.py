from fastapi import FastAPI
from app.api.v1.api import api_router


# from models import users
# from core.database import Base, engine
# from models import posts

# posts.Base.metadata.create_all(bind=engine)
# users.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(api_router)

@app.get("/", tags=["home"])
def home():
    return {"data": "Home page"}