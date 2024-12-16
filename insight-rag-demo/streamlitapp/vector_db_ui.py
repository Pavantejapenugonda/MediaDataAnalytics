import streamlit as st
import requests

UPLOAD_API = "http://127.0.0.1:9000/"

def create_vectordb():
    # Display buttons in a single row
    uploaded_files = st.file_uploader("Choose PDF files", type=["pdf"], accept_multiple_files=True)
    col1, col2 = st.columns(2)
    if col1.button("Upload"):
        if uploaded_files:
            with st.spinner("Uploading files..."):
                progress_bar = st.progress(0)  # Initialize progress bar
                total_files = len(uploaded_files)

                for idx, uploaded_file in enumerate(uploaded_files):
                    print(uploaded_file)
                    files = {"files": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    response = requests.post(UPLOAD_API + "upload_pdfs/", files=files)

                    if response.status_code == 200:
                        col2.success(f"{uploaded_file.name} uploaded successfully!")
                    else:
                        col2.error(f"Failed to upload {uploaded_file.name}.")

                    # Update progress bar
                    progress_bar.progress((idx + 1) / total_files)
            
            col2.success("All files uploaded!")
    elif col2.button("Reset"):
        with st.spinner("Reseting DB..."):
            response = requests.post(UPLOAD_API + "reset_database/")
            if response.status_code == 200:
                st.success(f"Sucessfully reseted the DB.")
            else:
                st.error(f"Failed to reset the DB.")
