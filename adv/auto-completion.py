import streamlit as st
import openai
import asyncio
import autogen
import os
from dotenv import load_dotenv
load_dotenv()

# OpenAI API key setup
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')



# Set up OpenAI client (Use your API key)
client = openai.OpenAI(api_key= OPENAI_API_KEY)

async def complete_code(user_code):
    response = await asyncio.to_thread(
        client.chat.completions.create,
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an AI assistant that autocompletes code."},
            {"role": "user", "content": f"Complete this code:\n{user_code}"}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content

# Streamlit UI
st.title("AI Code Autocomplete")

user_code = st.text_area("Start typing your code...", height=200)

if user_code:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    completed_code = loop.run_until_complete(complete_code(user_code))
    
    st.subheader("Autocompleted Code:")
    st.code(completed_code, language="python")
