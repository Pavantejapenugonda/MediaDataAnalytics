import streamlit as st
import base64
from vector_db_ui import create_vectordb
from rag_ui import query_vector_db, query_rag

# Use st.markdown to insert HTML for layout control
st.markdown(
    f'<div style="display: flex; align-items: center;">'
    f'<h1 style="margin-left: 20px;"> Insight Custom RAG Model</h1>'
    f'</div>',
    unsafe_allow_html=True
)

pg = st.navigation([
    st.Page(create_vectordb, title="Create Vector DB"),
    st.Page(query_vector_db, title="Query Vector DB"),
    st.Page(query_rag, title="Query RAG"),
])
pg.run()