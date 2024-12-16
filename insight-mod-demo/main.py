import streamlit as st
import base64
from audio_ui import audio_page
from image_ui import image_analysis_page
from video_ui import video_analysis_page
from rag_ui import query_rag

# Use st.markdown to insert HTML for layout control
st.markdown(
    f'<div style="display: flex; align-items: center;">'
    f'<h1 style="margin-left: 20px;"> Insight Media Analysis</h1>'
    f'</div>',
    unsafe_allow_html=True
)

pg = st.navigation([
    st.Page(audio_page, title="Audio Processing"),
    st.Page(image_analysis_page, title="Image Processing"),
    st.Page(video_analysis_page, title="Video Processing"),
    st.Page(query_rag, title="RAG Processing"),
])
pg.run()