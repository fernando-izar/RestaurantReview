from fastapi import FastAPI
from app.routes import review_routes

app = FastAPI()

app.include_router(review_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)