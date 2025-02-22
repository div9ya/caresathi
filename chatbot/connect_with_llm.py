import os
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Load API Token Securely
HF_TOKEN = os.getenv("HF_TOKEN")  # Set this in your environment variables
HUGGINGFACE_REPO_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

def load_llm(huggingface_repo_id):
    """Load the Hugging Face LLM model."""
    llm = HuggingFaceEndpoint(
        repo_id=huggingface_repo_id,
        temperature=0.5,
        huggingfacehub_api_token=HF_TOKEN, 
         task="text-generation", # Pass token correctly
        model_kwargs={"max_length": 512}  # Ensure `max_length` is an integer
    )
    return llm

# Define Custom Prompt
CUSTOM_PROMPT_TEMPLATE = """
Use the pieces of information provided in the context to answer user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer. 
Don't provide anything out of the given context.

Context: {context}
Question: {question}

Start the answer directly. No small talk please.
"""

def set_custom_prompt(custom_prompt_template):
    """Create a PromptTemplate instance."""
    return PromptTemplate(template=custom_prompt_template, input_variables=["context", "question"])

# Load FAISS Database
DB_FAISS_PATH = "vectorstore/db_faiss"
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

try:
    db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
except Exception as e:
    print(f"Error loading FAISS database: {e}")
    exit(1)

# Create Retrieval-based QA Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=load_llm(HUGGINGFACE_REPO_ID),
    chain_type="stuff",
    retriever=db.as_retriever(search_kwargs={'k': 3}),
    return_source_documents=True,
    chain_type_kwargs={'prompt': set_custom_prompt(CUSTOM_PROMPT_TEMPLATE)}
)

# Accept User Query
user_query = input("Write Query Here: ")
response = qa_chain.invoke({'query': user_query})  # Fixed key name
print("RESULT:", response.get("result", "No result found"))
