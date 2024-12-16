import streamlit as st
import requests, json
import cv2
import numpy as np
import base64

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def summarize_the_image(base64_images):
    headers = {'Content-Type': 'application/json'}
    prompt_text ="What is in this picture? in 100 words"
    url = "http://localhost:11434/api/generate"
    data = {"model": "llava", "prompt":prompt_text, "stream":False, "images": [base64_images]}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json()
            return result["response"]
        else:
            st.error(f"Error: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")

def image_analysis_page():
    # Display buttons in a single row
    col1, col2 = st.columns(2)

    # File uploader and language selection
    uploaded_file = col1.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None:
        # Convert the file to an opencv image.
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, 1)

        # Now do something with the image! For example, let's display it:
        col2.image(opencv_image, channels="BGR")
        if col1.button("Describe Image"):
            uploaded_file = "C:/Users/ppenugonda/Downloads/"+uploaded_file.name
            base64_images = image_to_base64(uploaded_file)
            reponse_txt = summarize_the_image(base64_images)
            col2.write(f"** Image description **: {reponse_txt}")
    else:
        col1.warning("Upload the Image file")