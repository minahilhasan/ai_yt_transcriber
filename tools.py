import streamlit as st
import requests
import google.genai as genai
from google.genai import types

def urlFinder(user_query):
    serpai_key = st.secrets["SERPAI"]["SERPAI_API_KEY"]

    params = {
        "engine": "youtube",
        "search_query": user_query,
        "api_key": serpai_key
    }

    response = requests.get("https://serpapi.com/search.json", params=params)
    if response.status_code != 200:
        return None

    results = response.json().get("video_results", [])
    if not results:
        return None

    return results[0]["link"] 

def videotranscriber(youtube_url):
    client = genai.Client(api_key=st.secrets["GEMINI"]["GEMINI_API_KEY"])

    response = client.models.generate_content(
        model='gemini-gemini-2.0-flash-lite', 
        contents=[
            types.Part.from_uri(
                file_uri=youtube_url,
                mime_type='video/mp4' 
            ),
            types.Part.from_text(text='Please provide a full, word-for-word transcription of this video.')
        ]
    )
    return response.text
