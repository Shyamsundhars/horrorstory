import os
import google.generativeai as genai
import streamlit as st 
import streamlit as st
import sys
import traceback

# Configure API Key
# Read API key from a file named 'api_key.txt'
try:
    with open(os.path.join(os.path.dirname(__file__), "api_key.txt"), "r") as f:
        api_key = f.read().strip()
except FileNotFoundError:
    st.error("API key file (api_key.txt) not found. Please create it in the same directory as the script.")
    sys.exit()
genai.configure(api_key = api_key)

generation_config = {
    "temperature": 0.75,
    "top_p":0.95,
    "top_k":40, 
    "max_output_tokens": 8192,
    "response_mime_type":"text/plain",   
}

#Initialize the generative model
model = genai.GenerativeModel(
    model_name = "gemini-1.5-flash",
    generation_config = generation_config,
)

#Define a function to to start the chat session with dynamic inputs
def generate_horror_story(character_name, situation, no_of_lines):
    try:
        prompt = (
            f"Write me a horror story with the chracter name \"{character_name}\" "
            f"and situatiion \"{situation} \" in {no_of_lines} lines."
        )
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb = traceback.extract_tb(exc_traceback)
        # Get the function name and line number from the traceback
        function_name = tb[-1].name
        line_number = tb[-1].line
        st.error(f"Error in function {function_name} at line {line_number}: {e}")
    
    #Start the chat session with the provided prompt
    chat_session = model.start_chat(
        history = [
            {
                "role":"user",
                "parts": [prompt],
            }
        ]
    )
    response = chat_session.send_message(prompt)
    return response.text

#Streamlit app interface
st.title("Horror Story Generator")
st.write("Enter the details below to generate your custom horror story: ")

#Inputs for the story
character_name = st.text_input("Character Name")
situation = st.text_input("Situation")
no_of_lines = int(st.number_input("Number of Lines", min_value=1, step=1))
no_of_lines = int(no_of_lines)

#Button to generate the story
if st.button("Generate Story"):
    with st.spinner("Generating your horror story..."):
        try:
            #st.write(type(no_of_lines))
            story = generate_horror_story(character_name, situation, no_of_lines)
            st.subheader("Your Horror Story:")
            st.write(story)
        except Exception as e:
            # Use traceback to get the line number and function
            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb = traceback.extract_tb(exc_traceback)
            # If you want the most recent frame (where the error was raised)
            function_name = tb[-1].name if tb else "unknown"
            line_number = tb[-1].line if tb else "unknown"
            st.error(f"An error occurred in function '{function_name}' at line {line_number}: {e}")