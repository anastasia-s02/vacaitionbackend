from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from firebaseInterface import getUserInfo
from recommendation_generator import generate_recommendation, generate_recs_for_two
import rerank
from modal import Stub, Secret
from modal import Image, Stub, asgi_app
import json

app = FastAPI()
stub = Stub()

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
    return json.dumps({"Hello": "World"})

@app.get("/plan/{u_id}")
def get_plan(u_id: str):
    # Fetch User Details
    user_details = getUserInfo(u_id)
    
    # Generate claude plan
    final = generate_recommendation([3500, 3700], 
                                    "2 weeks",
                                    ["get adrenaline rush", "immerse into new culture"], 
                                    "NYC",
                                    "sunny",
                                    "NA",
                                    "NA",
                                    "NA")
    
    return json.dumps({"u_id": u_id, "plan": final, "user_details": user_details})

@app.get("/couple_plan/{u_id1}")
def get_couple_plan(u_id1: str, u_id2: str):
    # Fetch User Details
    user_details1 = getUserInfo(u_id1)
    user_details2 = getUserInfo(u_id2)
    
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
    
    return json.dumps({"u_id1": u_id1, "u_id2": u_id2, "plan": final, "user_details1": user_details1, "user_details2": user_details2})

@app.get("/buddies/{u_id}")
def get_buddies(u_id: str):
    # Fetch User Details
    print("Fetching user details")
    user_details = getUserInfo(u_id)
    
    print("Getting buddies")
    # Find buddies based on similarity
    buddies = rerank.get_buddies(user_details)
    
    return json.dumps({"u_id": u_id, "buddies": buddies, "user_details": user_details})

image = Image.debian_slim().pip_install("boto3").pip_install("firebase_admin").pip_install("anthropic").pip_install("cohere")

@stub.function(image=image, secret=Secret.from_name("hackgpt"))
@asgi_app()
def fastapi_app():
    return app