from fastapi import FastAPI
from api.endpoints import router

app = FastAPI()

# Ajouter les routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
