from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses with friendly formatting
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    prompt = f"Hey there, curious explorer! I'm 10 year old kid! Today, you're curious about {question}, right? That's awesome! What exciting things do you already know about it, or is there something fun you'd like to learn first?"
    try:
        response = chat.send_message(prompt, stream=True)
        return response
    except Exception as e:  # Catch any exceptions that might lead to None responses
        print(f"Error occurred while getting response: {e}")
        return None  # Return None to prevent the iteration in the main code

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Initialize Streamlit app
st.set_page_config(page_title="Q&A Demo")
#st.image("img\img3.jpg", width=10, use_column_width=True)
st.header("Let's learn together with Coco🤩!")

# Input and submit button
input_text = st.text_input("What do you want to explore today?", key="input")
submit_button = st.button("Ask Coco")

# Process user input and get response
if submit_button and input_text:
    response = get_gemini_response(input_text)

    if response is not None:  # Check if response is not None before iterating
        # Add user query and response to session state chat history
        st.session_state['chat_history'].append(("You", input_text))

        st.subheader("The Response is")
        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))
    else:
        st.error("An error occurred while processing your request. Please try again later.")


st.subheader("Chat History:")

for role, text in st.session_state['chat_history']:
    if role == "You":
        st.write(f"**You:** {text}")  # Blue for user
    else:
        st.write(f"**Bot:** {text}")