import asyncio
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import mysql.connector
import unittest
import time

LOG_FILE = "test_results.txt"

def log_result(message):
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")
        
load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="xxxx",
        database="users"
    )

def create_pdf_record(user_id, pdf_name):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO pdfs (user_id, pdf_name) VALUES (%s, %s)",
            (user_id, pdf_name)
        )
        db.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        db.close()

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n
    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def store_history(user_id, pdf_id, question, answer):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO history (user_id, pdf_id, question, answer) VALUES (%s, %s, %s, %s)",
            (user_id, pdf_id, question, answer)
        )
        db.commit()
    finally:
        cursor.close()
        db.close()

def user_input(user_question, user_id, pdf_id):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain(
        {"input_documents": docs, "question": user_question},
        return_only_outputs=True
    )
    st.write("Reply: ", response["output_text"])
    if st.session_state.get("user") == "Guest":
        if "history" not in st.session_state:
            st.session_state.history = []
        st.session_state.history.append({"question": user_question, "answer": response["output_text"]})
    else:
        store_history(user_id, pdf_id, user_question, response["output_text"])

def main():
    st.header("Hello! Welcome to PDF Pulse💁")

    # Initialize session state variables
    if "user_id" not in st.session_state:
        st.session_state.user_id = None  # or some default value, like 1 for guest
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.get("user") == "Guest":
        if "history" not in st.session_state:
            st.session_state.history = []
    if "uploaded_pdf" not in st.session_state:
        st.session_state.uploaded_pdf = None

    pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
    
    if pdf_docs:  # Check if any files are uploaded
        uploaded_pdf = pdf_docs[0]  # Get the first file in the list
        file_details = {
            "filename": uploaded_pdf.name,
            "filetype": uploaded_pdf.type,
            "filesize": uploaded_pdf.size
        }
        user_id = st.session_state.user_id if st.session_state.logged_in else None
        pdf_id = create_pdf_record(user_id, file_details["filename"])  # Use file name from details
        st.session_state.pdf_id = pdf_id

    if st.button("Submit & Process"):
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            progress_bar.progress(percent_complete + 1)
        with st.spinner("Processing..."):
            raw_text = get_pdf_text([uploaded_pdf])  # Pass the list with the single file
            text_chunks = get_text_chunks(raw_text)
            get_vector_store(text_chunks)
            st.success("Done")

    user_question = st.text_input("Ask a Question from the PDF Files")
    user_id = st.session_state.get("user_id", 0)  # Default to 0 for guest user
    print(user_id)
    pdf_id = st.session_state.get("pdf_id", 0)  # Default to 0 if no PDF is uploaded

    if user_question:
        # user_input(user_question, user_id, pdf_id)
        start_time = time.time()
        response = user_input(user_question, user_id, pdf_id)
        end_time = time.time()
        response_time = end_time - start_time
        st.write(f"Response time: {response_time:.2f} seconds")
        log_result(f"Question: {user_question}, Response: {response}, Response time: {response_time:.2f} seconds")

if __name__ == "__main__":
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())
    main()

