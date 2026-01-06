from fastapi import FastAPI, APIRouter
import uvicorn

from database import router as db_router
from handlers import router as handlers_router
app = FastAPI()

main_router = APIRouter()
main_router.include_router(db_router)
main_router.include_router(handlers_router)

app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)


