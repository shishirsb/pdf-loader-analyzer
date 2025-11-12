from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_community.document_loaders import PyMuPDFLoader
import io
import tempfile
import os
from interface.api import API

class RAGTool:
    """Retrieval-Augmented Generation (RAG) tool for analyzing PDF documents."""

    def __init__(self, pdf_bytes: bytes):
        """
        Initialize the RAG tool with the given PDF file bytes.

        Args:
            pdf_bytes (bytes): The uploaded PDF file content.
        """
        self.api_interface = API()
        self.api_interface.set_api_key()

        self.pdf_bytes = pdf_bytes

        # Process the document through extraction, chunking, and embedding
        self.pages = self._extract_text_from_pdf()
        self.chunks = self._break_down_documents_into_chunks()
        self.vector_store = self._build_vector_store()

    # -----------------------------------------------------------------------
    # Internal helper methods
    # -----------------------------------------------------------------------

    def _extract_text_from_pdf(self):
        """Extract text from the uploaded PDF file."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(self.pdf_bytes)
            temp_file_path = temp_file.name

        try:
            loader = PyPDFLoader(temp_file_path)
            pages = loader.load_and_split()
            return pages
        finally:
            os.remove(temp_file_path)
        
    def _break_down_documents_into_chunks(self):
        """Break down the extracted pages into smaller chunks."""
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        chunks = text_splitter.split_documents(self.pages)
        return chunks
    
    def _build_vector_store(self):
        """Build a vector store from the document chunks."""
        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_documents(self.chunks, embeddings)
        return vector_store
    
    # -----------------------------------------------------------------------
    # Public method
    # -----------------------------------------------------------------------

    def ask(self, query):
        """
        Ask a question about the uploaded document using retrieval-augmented generation.

        Args:
            query (str): The question to ask.

        Returns:
            str: The model's response.
        """

        llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)

        # Retrieve top relevant chunks
        similar_docs = self.vector_store.similarity_search(query, k=3)
        context_text = "\n\n".join([doc.page_content for doc in similar_docs])

        # Build structured prompt
        prompt_template = """You are a legal assistant helping summarize legal documents. 
        # Using the context below, answer the question concisely and accurately.
        # Context: {context}
        # Question: {query}"""

        prompt = prompt_template.format(context=context_text, query=query)
        response = llm.invoke(prompt)
        return response

def analyze_document(input_data: dict) -> str:
    """
    Analyze a PDF document and answer a query using RAG.

    Args:
        input_data (dict): Dictionary with 'pdf_file' (bytes) and 'query' (str).

    Returns:
        str: Model response content.
    """
    legal_doc_analyzer = RAGTool(input_data['pdf_file'])
    response = legal_doc_analyzer.ask(input_data['query'])
    return response.content