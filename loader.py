

from langchain_community.document_loaders import PyPDFLoader

def load_pdf(file_path):
    """
    Load a PDF and return all pages
    """
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    # Add book name to each document
    book_name = file_path.split("/")[-1].replace(".pdf", "")
    for doc in documents:
        doc.metadata["book_name"] = book_name
    
    return documents

def load_multiple_pdfs(file_paths):
    """
    Load multiple PDFs
    """
    all_docs = []
    for file_path in file_paths:
        try:
            docs = load_pdf(file_path)
            all_docs.extend(docs)
            print(f"Loaded: {file_path}")
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    return all_docs

