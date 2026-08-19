# # py->gem api->ai res (the below code is to check if the gemini api is working properly)
# import os

# from dotenv import load_dotenv
# from google import genai


# load_dotenv()

# api_key = os.getenv("GEMINI_API_KEY")

# if not api_key:
#     raise ValueError("GEMINI_API_KEY was not found in the .env file.")


# client = genai.Client(api_key=api_key)


# response = client.models.generate_content(
#     model="gemini-3.6-flash",
#     contents="Explain inheritance in Java in simple terms."
# )


# print(response.text)


##concerting program with streamlit
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai


# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY was not found in the .env file.")
    st.stop()

# Create Gemini client
client = genai.Client(api_key=api_key)


# Configure Streamlit page
st.set_page_config(
    page_title="DevLearn AI",
    page_icon="🤖"
)


# Application title
st.title("🤖 DevLearn AI")
st.subheader("AI-Powered Study & Coding Assistant")


# User input
question = st.text_input(
    "Ask a question"
)


# Ask AI button
if st.button("Ask AI"):

    if question:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=question
        )

        st.write(response.text)

    else:

        st.warning("Please enter a question.")