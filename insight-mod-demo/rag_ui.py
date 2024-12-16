import streamlit as st
import pandas as pd
import requests
QUERY_RAG_API = "http://127.0.0.1:7000/"

# Function to fetch results from the API
def fetch_results_from_api(query_api, user_query, top_k=0):
    try:
        headers = {'Content-Type': 'application/json'}
        json_query = {"query_text": user_query}
        if top_k:
            json_query['top_k'] = top_k
        
        response = requests.post(query_api, json=json_query, headers= headers)
        if response.status_code == 200:
            # Parse the JSON response to get the data
            data = response.json()
            return data['response']  # Assuming the response key is 'response'
        else:
            st.error("Failed to fetch data from the API.")
            return []
    except Exception as e:
        st.error(f"Error occurred while fetching data: {str(e)}")
        return []
    
def query_vector_db():
    # Input for user query
    user_query = st.text_input("Enter your query:")
    # Select top K using Streamlit slider
    k = st.slider("Select Top K", min_value=1, max_value=10)
    if st.button("Fetch"):
        # Fetch results from the API
        api_results = fetch_results_from_api(QUERY_RAG_API+"query_vdb/", user_query, k)
        if api_results:
            # Convert the API response to a DataFrame for easy display in a table
            df = pd.DataFrame(api_results)
            # Display the DataFrame as a table
            st.subheader("Results")
            st.table(df)  # You can use st.dataframe(df) for interactive scrolling and sorting
        else:
            st.info("No results to display.")
            
def query_rag():
    # Input for user query
    user_query = st.text_input("Enter your query:")
    k = st.slider("Select Top K", min_value=1, max_value=10)
    if st.button("Submit Query"):
        if user_query:
            # Make a POST request to the RAG API
            response = requests.post(QUERY_RAG_API+"query_rag/", json={"query_text": user_query, "top_k":k})

            if response.status_code == 200:
                response_data = response.json()
                st.write("### Response:")
                st.write(response_data.get("response", "No response"))
                st.write("### Sources:")
                st.write(response_data.get("sources", "No sources"))
            else:
                st.error("Failed to retrieve the answer from the RAG system.")
        else:
            st.warning("Please enter a query.")