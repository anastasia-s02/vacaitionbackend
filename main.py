from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from firebaseInterface import getUserInfo
from recommendation_generator import generate_recommendation, generate_recs_for_two
import rerank

app = FastAPI()

origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/plan/{u_id}")
def get_plan(u_id: str):
    # Fetch User Details
    user_details = getUserInfo(u_id)
    
    # Generate claude plan
    final = generate_recommendation([3500, 3700], 
                                    "2 weeks",
                                    ["get adrenaline rush", "immerse into new culture"], 
                                    "NYC", 
                                    "plane",
                                    "sunny",
                                    avoid_list="NA")
    
    return {"u_id": u_id, "plan": final, "user_details": user_details}

@app.get("/couple_plan/{u_id}")
def get_couple_plan(u_id: str):
    # Fetch User Details
    user_details = getUserInfo(u_id)
    
    # Generate claude plan
    final = generate_recs_for_two([3500, 3700], 
                                    "2 weeks",
                                    ["get adrenaline rush", "immerse into new culture"], 
                                    "NYC", 
                                    "plane",
                                    "sunny",
                                    "NA",
                                    [3500, 3700], 
                                    "2 weeks",
                                    ["get adrenaline rush", "immerse into new culture"], 
                                    "NYC", 
                                    "plane",
                                    "sunny",
                                    "NA")
    
    return {"u_id": u_id, "plan": final, "user_details": user_details}

@app.get("/buddies/{u_id}")
def get_buddies(u_id: str):
    # Fetch User Details
    print("Fetching user details")
    user_details = getUserInfo(u_id)
    
    print("Getting buddies")
    # Find buddies based on similarity
    buddies = rerank.get_buddies(user_details)
    
    return {"u_id": u_id, "buddies": buddies, "user_details": user_details}