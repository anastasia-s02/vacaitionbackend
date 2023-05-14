import cohere, os
from environment import ENVIRONMENT

# Get your cohere API key on: www.cohere.com
co = cohere.Client(os.environ["COHERE_KEY"])

# Example query and passages
# query = "I like to do hiking and going to the beach"

# use rerank to get the top buddies from their preferences and comments
# There are hard restrictions and then their are soft restrictions where we rank the top 3
def get_buddies(user_info):
    # Need to use the user_info to get the preferences and comments
    query = "I like to do hiking and going to the beach"
    results = co.rerank(query=query, documents=[
        "I am a movie buff and I love to watch movies",
        "I am a foodie and I love to eat food",
        "I am a gamer and I love to play games",
        "I am a bookworm and I love to read books",
        "I am a music lover and I love to listen to music",
        "I am a sports fan and I love to watch sports",
        "I like to go out and party",
        "I am a nature lover and I love to go out and explore nature",
        ], top_n=3, model="rerank-multilingual-v2.0")

    return results