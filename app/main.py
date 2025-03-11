from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json
from app.routers.jsonRouter import jsonRouter
from app.routers.pandasRouter import pandasRouter

app = FastAPI()

# Add CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the root path
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Include the JSON router
routers = [jsonRouter, pandasRouter]
for router in routers:
    app.include_router(router)


