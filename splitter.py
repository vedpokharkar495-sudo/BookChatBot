


from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_into_chunks(documents, chunk_size=1000, chunk_overlap=200):
    """
    Split documents into smaller chunks
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks from {len(documents)} pages")
    
    return chunks
    
    
    