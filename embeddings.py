

from langchain_huggingface import HuggingFaceEmbeddings

# Initialize embeddings once
embeddings_model = None

def get_embeddings_model():
    """
    Get or create embeddings model
    """
    global embeddings_model
    if embeddings_model is None:
        print("Loading embedding model...")
        embeddings_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
    return embeddings_model

def create_embeddings(texts):
    """
    Create embeddings for a list of texts
    """
    model = get_embeddings_model()
    return model.embed_documents(texts)

def embed_question(question):
    """
    Create embedding for a single question
    """
    model = get_embeddings_model()
    return model.embed_query(question)
    

