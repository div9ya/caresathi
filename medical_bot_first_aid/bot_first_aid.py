import os
import streamlit as st

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint

## Uncomment the following files if you're not using pipenv as your virtual environment manager
#from dotenv import load_dotenv, find_dotenv
#load_dotenv(find_dotenv())


DB_FAISS_PATH="vectorstore/db_faiss"
@st.cache_resource
def get_vectorstore():
    embedding_model=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    db=FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
    return db


def set_custom_prompt(custom_prompt_template):
    prompt=PromptTemplate(template=custom_prompt_template, input_variables=["context", "question"])
    return prompt


def load_llm(huggingface_repo_id, HF_TOKEN):
    llm = HuggingFaceEndpoint(
        repo_id=huggingface_repo_id,
        temperature=0.5,
        huggingfacehub_api_token=HF_TOKEN,  # Correct token placement
        task="text-generation",
        model_kwargs={"max_length": 512}  # Ensure max_length is an integer
    )
    return llm



def main():
    st.title("GET YOUR FIRST AID!")

    

    prompt=st.chat_input("ENTER THE CONDITION")

    if prompt:
        st.chat_message('user').markdown(prompt)

        CUSTOM_PROMPT_TEMPLATE = """
            Use the pieces of information provided in the context to Provide clear and concise first aid instructions for the question provided . Ensure the steps are easy to follow, medically accurate, and suitable for immediate response before professional help arrives. If necessary, include precautions and warnings to avoid worsening the condition. Format the response in a structured step-by-step manner..
            If you don't know the answer, just say that you don't know, don't try to make up an answer. 
            Don't provide anything out of the given context.

            Context: {context}
            Question: {question}

            Start the answer directly. No small talk please.
            """
        
        HUGGINGFACE_REPO_ID="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        HF_TOKEN=os.environ.get("HF_TOKEN")

        try: 
            vectorstore=get_vectorstore()
            if vectorstore is None:
                st.error("Failed to load the vector store")

            qa_chain=RetrievalQA.from_chain_type(
                llm=load_llm(huggingface_repo_id=HUGGINGFACE_REPO_ID, HF_TOKEN=HF_TOKEN),
                chain_type="stuff",
                retriever=vectorstore.as_retriever(search_kwargs={'k':3}),
                return_source_documents=True,
                chain_type_kwargs={'prompt':set_custom_prompt(CUSTOM_PROMPT_TEMPLATE)}
            )

            response=qa_chain.invoke({'query':prompt})

            result=response["result"]
            source_documents=response["source_documents"]
            result_to_show=result
            #response="Hi, I am MediBot!"
            st.chat_message('assistant').markdown(result_to_show)
            

        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()