from typing import Union
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from firebaseInterface import getUserInfo
# , getQuestionnaire
from recommendation_generator import generate_recommendation, generate_recs_for_two
import rerank
from modal import Stub, Secret
from modal import Image, Stub, asgi_app
import json
import os
from dotenv import load_dotenv

load_dotenv()

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

@app.get("/user/{u_id}")
def get_user(u_id: str):
    # Fetch User Details
    user_details = getUserInfo(u_id)
    
    return json.dumps({"u_id": u_id, "user_details": user_details})

@app.get("/questionnaire/{u_id}")
def get_questionnaire(u_id: str):
    # Fetch User Details
    quest = getQuestionnaire(u_id)
    
    return json.dumps({"u_id": u_id, "questionnaire": quest})

# below code runs when the frontend Questionnaire is submitted
# @app.get("/plan/{u_id}")
@app.post("/plan")
# def get_plan(u_id: str):
async def get_plan(request: Request):
    print("/plan/ was called")

    # Retrieve the request body
    data = await request.json()
    print("data: ", data)
    # Fetch User Details
    # print("user_id: ", u_id)
    # user_details = getUserInfo(u_id)
    # print("user_details: ", user_details)
    # quest = getQuestionnaire(u_id)
    # print("quest: ", quest)
    
    # Extract the necessary data from the request body
    budget = data.get("budget")
    duration = data.get("duration")
    time = data.get("time")
    departFrom = data.get("departFrom")
    weather = data.get("weather")
    avoid = data.get("avoid")
    additionalInfo = data.get("additionalInfo")
    countries = data.get("countries")
    
    # Generate claude plan
    final = generate_recommendation(budget, duration, time, departFrom, weather, avoid, additionalInfo, countries)
    
    return json.dumps({"plan": final})

    # Generate claude plan
    # final = generate_recommendation(quest["budget"],
    #                                 quest["duration"],
    #                                 quest["time"], 
    #                                 quest["departFrom"],
    #                                 quest["weather"],
    #                                 quest["avoid"],
    #                                 quest["additionalInfo"],
    #                                 quest["countries"])
    
    # return json.dumps({"u_id": u_id, "plan": final})

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
    print(user_details)
    
    print("Getting buddies")
    # Find buddies based on similarity
    buddies = rerank.get_buddies(u_id, user_details)
    print(buddies[0].document['text'])
    
    return json.dumps({"u_id": u_id, "buddies": buddies[0].document['text']})

image = Image.debian_slim().pip_install("boto3").pip_install("firebase_admin").pip_install("anthropic").pip_install("cohere")

@stub.function(image=image, secret=Secret.from_name("hackgpt"))
@asgi_app()
def fastapi_app():
    return app