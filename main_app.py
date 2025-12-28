import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from pdf_handler import extract_text_from_pdf
from text_processing import split_text_into_documents
from vector_store import create_vectorstore, get_retriever
from workflow_manager import create_workflow

def build_app():
    """
    Orchestrates the loading of data and creation of the graph.
    Returns the compiled workflow app.
    """
    # Path to the PDF file
    pdf_path = "input.pdf"
    
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file '{pdf_path}' not found. Please add it to the directory.")

    print(f"--- Processing {pdf_path} ---")
    
    # Extract text from the PDF
    pdf_text = extract_text_from_pdf(pdf_path)

    # Split the text into Document objects
    doc_splits = split_text_into_documents(pdf_text)

    # Add to vector store
    print("--- Creating Vector Store ---")
    vectorstore = create_vectorstore(
        documents=doc_splits,
        collection_name="rag-chroma",
        persist_directory="./chroma_db",
    )
    retriever = get_retriever(vectorstore)

    # Create the workflow
    print("--- Compiling Workflow ---")
    app = create_workflow(retriever)
    
    return app

# Allow direct execution for testing
if __name__ == "__main__":
    try:
        app = build_app()
        print("Workflow compiled successfully!")
    except Exception as e:
        print(f"Error: {e}")