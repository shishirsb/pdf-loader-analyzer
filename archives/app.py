import streamlit as st
from process_document import RAG_Tool
import os
os.environ["OPENAI_API_KEY"] = "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"


#Add Upload document form
st.title("Document Analyzer")

with st.form("upload form"):
    uploaded_file = st.file_uploader("Upload a pdf file", type = ['pdf'])
    query = st.text_input("Enter your query (e.g., What is the purpose of this document?)")
    submitted = st.form_submit_button("Submit")

if submitted:
    if uploaded_file is not None:
        #Load pdf
        st.write("..Processing ..")
        legal_doc_analyzer = RAG_Tool(uploaded_file) #Use Case
        response = legal_doc_analyzer.ask(query)
        st.write(response.content)
elif uploaded_file is None:
    st.write("Please upload a pdf document to analyze!")

    
