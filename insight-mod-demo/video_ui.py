import streamlit as st
import requests, json

def describe_the_video(filename):
    headers = {'Content-Type': 'application/json'}
    url = "https://ane87afbzu-496ff2e9c6d22116-5000-colab.googleusercontent.com/"
    data = {"video_filename": filename}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result["response"]
        else:
            st.error(f"Error: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")

def video_analysis_page():
    # Display buttons in a single row
    col1, col2 = st.columns(2)
    uploaded_file = col1.file_uploader("Choose an video file", type=['mp4'])
    if uploaded_file is not None:
        # Display the video in the UI
        col2.video(uploaded_file)
        if col1.button("Submit"):
            # Display selected point details
            #response_txt = describe_the_video(uploaded_file)
            response_txt = "A video car driving on the highway, with one car infront of the others. The camera captures the scence from the back of the car in infront"
            col1.write(f"**Video Content : {response_txt}**")