from unittest.mock import patch, MagicMock
from application.document_analyzer import RAGTool, analyze_document


# ----------------------------------------------------------------------
# ✅ POSITIVE TEST CASE: Full successful run
# ----------------------------------------------------------------------
@patch("application.document_analyzer.PyPDFLoader")
@patch("application.document_analyzer.FAISS")
@patch("application.document_analyzer.OpenAIEmbeddings")
@patch("application.document_analyzer.ChatOpenAI")
def test_rag_tool_ask_success(mock_chat, mock_embeddings, mock_faiss, mock_loader):
    """Test RAGTool.ask() end-to-end with mocked dependencies."""

    # ✅ Use a real Document object instead of MagicMock
    from langchain_core.documents import Document

    mock_loader_instance = MagicMock()
    mock_loader_instance.load_and_split.return_value = [
        Document(page_content="This is fake page content", metadata={})
    ]
    mock_loader.return_value = mock_loader_instance

    # Mock FAISS vector store
    mock_vector_store = MagicMock()
    mock_vector_store.similarity_search.return_value = [
        Document(page_content="Relevant legal text A", metadata={}),
        Document(page_content="Relevant legal text B", metadata={}),
    ]
    mock_faiss.from_documents.return_value = mock_vector_store

    # Mock ChatOpenAI model
    mock_llm_instance = MagicMock()
    mock_llm_instance.invoke.return_value.content = "Mocked AI legal summary"
    mock_chat.return_value = mock_llm_instance

    # Instantiate RAGTool
    tool = RAGTool(pdf_bytes=b"%PDF-fake")
    result = tool.ask("Summarize the agreement.")

    # Assertions
    mock_loader.assert_called_once()
    mock_faiss.from_documents.assert_called_once()
    mock_chat.return_value.invoke.assert_called_once()
    assert isinstance(result.content, str)
    assert "Mocked AI" in result.content

