from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json
from app.routers.jsonRouter import jsonRouter

app = FastAPI()

# Add CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the JSON router
routers = [jsonRouter]
for router in routers:
    app.include_router(router)


