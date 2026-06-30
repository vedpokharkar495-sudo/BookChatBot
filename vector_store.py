


from langchain_community.vectorstores import FAISS
import os
import pickle

# Store active vector stores
active_stores = {}

def create_vector_store(chunks, book_name):
    """
    Create and save vector store for a book
    """
    from embeddings import get_embeddings_model
    
    print(f"Creating vector store for {book_name}...")
    
    embeddings = get_embeddings_model()
    vector_store = FAISS.from_documents(chunks, embeddings)
    
    # Save to disk
    save_path = f"vector_db/{book_name}"
    vector_store.save_local(save_path)
    
    # Keep in memory
    active_stores[book_name] = vector_store
    
    print(f"Vector store created with {len(chunks)} chunks")
    return vector_store

def load_vector_store(book_name):
    """
    Load vector store from disk
    """
    from embeddings import get_embeddings_model
    
    # Check if already loaded
    if book_name in active_stores:
        return active_stores[book_name]
    
    # Load from disk
    load_path = f"vector_db/{book_name}"
    
    if not os.path.exists(load_path):
        print(f"No vector store found for {book_name}")
        return None
    
    try:
        embeddings = get_embeddings_model()
        vector_store = FAISS.load_local(
            load_path, 
            embeddings,
            allow_dangerous_deserialization=True
        )
        active_stores[book_name] = vector_store
        print(f"Loaded vector store for {book_name}")
        return vector_store
    except Exception as e:
        print(f"Error loading vector store: {e}")
        return None

def search_similar_chunks(book_name, question, k=4):
    """
    Search for chunks similar to the question
    """
    vector_store = load_vector_store(book_name)
    
    if vector_store is None:
        return []
    
    results = vector_store.similarity_search(question, k=k)
    return results

def delete_vector_store(book_name):
    """
    Delete vector store from memory and disk
    """
    import shutil
    
    # Remove from memory
    if book_name in active_stores:
        del active_stores[book_name]
    
    # Remove from disk
    store_path = f"vector_db/{book_name}"
    if os.path.exists(store_path):
        shutil.rmtree(store_path)
        print(f"Deleted vector store: {book_name}")


