


from transformers import pipeline

# Global LLM pipeline
llm_pipeline = None

def get_llm():
    """
    Get or create LLM pipeline
    """
    global llm_pipeline
    
    if llm_pipeline is None:
        print("Loading LLM model... (this might take a minute)")
        llm_pipeline = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",
            max_length=500,
            temperature=0.1
        )
    
    return llm_pipeline

def create_prompt(context, question, prompt_type="general"):
    """
    Create prompt based on question type
    """
    if prompt_type == "quiz":
        prompt = f"""Based on this book content, create a quiz.

Context:
{context}

Request: {question}

Generate 5 multiple choice questions with answers. Format each question clearly.

Quiz:"""
    
    elif prompt_type == "summary":
        prompt = f"""Summarize this book content.

Context:
{context}

Request: {question}

Provide a clear summary:

Summary:"""
    
    elif prompt_type == "interview":
        prompt = f"""Based on this book content, generate interview questions.

Context:
{context}

Request: {question}

Generate 5 interview questions with answers:

Interview Questions:"""
    
    else:  # general
        prompt = f"""Answer the question based on the book content below.

Book Content:
{context}

Question: {question}

Answer (be specific and use information from the content):"""
    
    return prompt

def answer_question(book_name, question, prompt_type="general"):
    """
    Main function to answer questions using RAG
    """
    import vector_store as vs
    
    # Step 1: Get relevant chunks
    relevant_chunks = vs.search_similar_chunks(book_name, question, k=4)
    
    if not relevant_chunks:
        return {
            "answer": "No relevant content found. Please upload a book first.",
            "sources": [],
            "chunks": []
        }
    
    # Step 2: Combine chunks into context
    context = "\n\n---\n\n".join([chunk.page_content for chunk in relevant_chunks])
    
    # Step 3: Get source pages
    sources = []
    for chunk in relevant_chunks:
        page = chunk.metadata.get('page', 'unknown')
        if page not in sources:
            sources.append(f"Page {page}")
    
    # Step 4: Create prompt
    prompt = create_prompt(context, question, prompt_type)
    
    # Step 5: Get answer from LLM
    try:
        llm = get_llm()
        response = llm(prompt, max_length=500)[0]['generated_text']
    except Exception as e:
        # Fallback if LLM fails
        response = f"Based on the book content:\n\n{context[:500]}..."
    
    # Step 6: Return everything
    return {
        "answer": response,
        "sources": sources,
        "chunks": [chunk.page_content[:200] + "..." for chunk in relevant_chunks]
    }

def process_book(file_path):
    """
    Complete pipeline: Load -> Split -> Embed -> Store
    """
    import loader
    import splitter
    import vector_store as vs
    
    # Step 1: Load PDF
    print(f"Loading PDF: {file_path}")
    documents = loader.load_pdf(file_path)
    
    # Step 2: Split into chunks
    print("Splitting into chunks...")
    chunks = splitter.split_into_chunks(documents)
    
    # Step 3 & 4: Create and store embeddings
    book_name = file_path.split("/")[-1].replace(".pdf", "")
    vs.create_vector_store(chunks, book_name)
    
    print(f"✅ Book processed successfully: {book_name}")
    return book_name


