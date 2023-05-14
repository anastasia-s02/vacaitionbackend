import os
import anthropic
import json
from environment import ENVIRONMENT


def generate_recommendation(budget: str, duration: str, activities: list[str], 
                            start_location: str, weather: str, avoid_list: str, additional_info: str, passport: str):
    
    c = anthropic.Client(os.environ["CLAUDE_KEY"])
    while True:
        try:
            resp = c.completion(
                prompt=f"{anthropic.HUMAN_PROMPT} Give me 3 vacation destinations (name of the city and the country, along with budget breakdown" +
                f"(transportation, hotel, and other expenses) and 5 activities for each destination) that fit these criteria: strict budget limit is " +
                f"${budget} for {duration} (including transportation from {start_location} -- state the estimated price for it ), I want the weather to be " +
                f"{weather}, the goals are {', '.join(activities)}, and I hold {passport} passport (I want easy entry). Here are the places I do not want to " +
                f"visit: {avoid_list}. {additional_info} Tip: if the budger is small to take a flight, consider destinations reachable by train or car from {start_location}.{anthropic.AI_PROMPT}",
                stop_sequences=[anthropic.HUMAN_PROMPT],
                model="claude-v1",
                max_tokens_to_sample=650,
            )
            response_final = c.completion(
                prompt=f"{anthropic.HUMAN_PROMPT} I want you to return me this same text but in the following format:" +
                f" {{\"name of location1\": \"all the rest of information about this location1\", \"name of location2\":" +
                f" \"all the rest of information about this location2\", \"name of location3\": \"all the rest of information " +
                f"about this location3\"}}. Give it to me in the exact format I specified. Keep all the escape sequences. Here is the text with 3 locations: {resp['completion']}{anthropic.AI_PROMPT}",
                stop_sequences=[anthropic.HUMAN_PROMPT],
                model="claude-v1",
                max_tokens_to_sample=650,
            )
            index = response_final['completion'].find('{')  
            new_text = response_final['completion'][index:]
            string = new_text.replace("'", "\"")
            final = json.loads(string)
            break
        except:
            pass
    return final

def generate_recs_for_two(budget1: str, duration1: str, activities1: list[str], 
                        start_location1: str, weather1: str, avoid_list1: str, additional_info1: str, passport1: str,
                        budget2: str, duration2: str, activities2: list[str], 
                        start_location2: str, weather2: str, avoid_list2: str, additional_info2: str, passport2: str):

    c = anthropic.Client(os.environ["CLAUDE_KEY"])
    while True:
        try:
            resp = c.completion(
                prompt=f"{anthropic.HUMAN_PROMPT} Give me 3 vacation destinations (name of the city and the country, along with budget breakdown" +
                "(transportation for each person, hotel for two, and other expenses per person) and 5 activities for each destination) for two people" +
                f"who request the following: budget limit for person 1 is {budget1} and for person 2 is {budget2} for {duration1} - {duration2} " +
                f"(including transportation from {start_location1} for person 1 and from {start_location2} for person 2), the goals are {', '.join(activities1)}"+
                f" {', '.join(activities2)}, and they hold {passport1}, {passport2} passports. Here are the places they want to avoid: {avoid_list1}, {avoid_list2}." +
                f"Tip: if the budgets are too small to take a flight, consider destinations reachable by train of car from both {start_location1} and {start_location2} {anthropic.AI_PROMPT}",
                stop_sequences=[anthropic.HUMAN_PROMPT],
                model="claude-v1",
                max_tokens_to_sample=800,
            )
            response_final = c.completion(
                prompt=f"{anthropic.HUMAN_PROMPT} I want you to return me this same text but in the following format:" +
                f" {{\"name of location1\": \"all the rest of information about this location1\", \"name of location2\":" +
                f" \"all the rest of information about this location2\", \"name of location3\": \"all the rest of information " +
                f"about this location3\"}}. Give it to me in the exact format I specified. Keep all the escape sequences. Here is the text with 3 locations: {resp['completion']}{anthropic.AI_PROMPT}",
                stop_sequences=[anthropic.HUMAN_PROMPT],
                model="claude-v1",
                max_tokens_to_sample=650,
            )
            index = response_final['completion'].find('{')  
            new_text = response_final['completion'][index:]
            string = new_text.replace("'", "\"")
            final = json.loads(string)
            break
        except:
            pass
    return final


