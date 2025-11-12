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


class RAG_Tool:
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file
        self.pages = self.extract_document()
        self.split_docs = self.chunk()
        self.library = self.load_embeddings()

    def extract_document(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(self.pdf_file.read())
            temp_file_path = temp_file.name
            loader = PyPDFLoader(temp_file_path)
            return loader.load_and_split()
        
    def chunk(self):
        #chunking the document
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        return text_splitter.split_documents(self.pages)
    
    def load_embeddings(self):
        #load embeddings
        embeddings = OpenAIEmbeddings()
        library = FAISS.from_documents(self.split_docs, embeddings)
        return library
    
    def ask(self, query):
        #retrieve answer
        llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)

        context = self.library.similarity_search(query, k=3)

        prompt = f"""You are a legal assistant helping summarize legal documents. 
        # Using the context below, answer the question concisely and accurately.
        # Context: {context}
        # Question: {query}"""

        return llm.invoke(prompt)


    


    