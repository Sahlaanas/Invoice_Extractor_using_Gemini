from dotenv import load_dotenv

load_dotenv() # load all the environment variable from .env

import streamlit as st

import os #os will be basically useful for picking up the environment variable ,assigning the environment variable from somewhere else

from PIL import Image

import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input, image, prompt):
    response = model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type" : uploaded_file.type,
                "data" : bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    


#initialize the streamlit setup

st.set_page_config(page_title="Multilanguage Invoice Extractor")
st.header("Multilanguage Invoice Extractor")

input = st.text_input("Input prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image of the Invoice ", type=["jpg","jpeg","png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Extract from the Invoice")

input_prompt = """
You are an expert in understanding invoices. We will upload an image as invoice 
and you will have to answer any question based on the uploaded invoice image
"""

# If submit button is clicked

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt,image_data,input)
    st.subheader("The response is: ")
    st.write(response)