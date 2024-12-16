import streamlit as st
import requests, json
import base64
import matplotlib.pyplot as plt
from wordcloud import WordCloud

lang_mapping_dict = {"English":"en", "Spanish":"es", "Arabic":"ar"}


def hit_audio_processing_api(endpoint, audio_file_path, translate_lang_code=None):
    url = f'http://localhost:8000/{endpoint}/'
    if translate_lang_code:
        data = {"audio_file": audio_file_path, 'translate_lang_code': translate_lang_code}
    else:
        data = {"audio_file": audio_file_path}
    try:
        response = requests.post(url, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json()
            return result[endpoint+'_text']
        else:
            st.error(f"Error: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")

def get_key_by_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None

def summarize_the_content(result):
    prompt_text = result + " Summarize the content"
    url = "http://localhost:11434/api/generate"
    data = {"model": "mistral", "prompt":prompt_text, "stream":False}
    try:
        response = requests.post(url, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json()
            return result["response"]
        else:
            st.error(f"Error: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")

def create_word_cloud(text):
    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    # Plotting the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    # plt.title('Word Cloud Example')
    return plt

def audio_page():
    # Display buttons in a single row
    col1, col2 = st.columns(2)

    # File uploader and language selection
    uploaded_file = col1.file_uploader("Choose an audio file", type=['wav', 'mp3', 'm4a', '.flac'])
    # translate_lang_code = col1.selectbox("Select translation language:", ["None", 'English', 'Spanish', 'Arabic'])

    if uploaded_file is not None:
        col2.audio(uploaded_file, format='audio/' + uploaded_file.type.split('/')[1])
        uploaded_file = r"C:/Users/ppenugonda/Downloads/" + uploaded_file.name
        if col1.button("Process"):
            result = hit_audio_processing_api("detect-language", uploaded_file)
            if result:
                col2.write(f"**Detected Language**: {get_key_by_value(lang_mapping_dict, result)}")
            result = hit_audio_processing_api("transcribe", uploaded_file)
            if result:
                col2.write(f"**Transcription**: {result}")
            result = hit_audio_processing_api("translate", uploaded_file, "en")
            if result:
                col2.write(f"**Translated Text**: {result}")
                summarize_txt = summarize_the_content(result)
                col2.write(f"**Summarized Text**: {summarize_txt}")
            col1.write("**Word Cloud**")
            word_cloud_plot = create_word_cloud(result)
            col1.pyplot(word_cloud_plot)
            col2.write("\n\n\n\n\n\n")
    else:
        col1.warning("Upload the audio file")