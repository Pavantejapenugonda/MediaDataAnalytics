from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from get_embedding_function import get_embedding_function

# Initialize FastAPI
app = FastAPI()

CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

# Define Pydantic model for request body
class QueryRequest(BaseModel):
    query_text: str
    top_k: int

@app.post("/query_vdb/")
async def query_vector_database(query_request: QueryRequest):
    try:
        query_text, top_k_val = query_request.query_text, query_request.top_k
        embedding_function = get_embedding_function()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

        # Search the DB.
        results = db.similarity_search_with_score(query_text, k=top_k_val)
        return {"response": [{"DocumentId" : ele[0].metadata['id'], "PageNo": ele[0].metadata['page'], "SourceText":ele[0].page_content, "Score":ele[1]} for ele in results]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/query_rag/")
async def query_rag_api(query_request: QueryRequest):
    try:
        query_text, top_k_val = query_request.query_text, query_request.top_k
        # Prepare the DB.
        embedding_function = get_embedding_function()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

        # Search the DB.
        results = db.similarity_search_with_score(query_text, k=top_k_val)
        # Extract context from the search results
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)

        # Query the model
        model = Ollama(model="mistral")
        response_text = model.invoke(prompt)

        # Get source documents
        sources = [doc.metadata.get("id", None) for doc, _score in results]
        formatted_response = {
            "response": response_text,
            "sources": sources
        }

        return formatted_response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7000)
