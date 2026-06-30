


import streamlit as st
import requests
import os

# API URL
API_URL = "http://localhost:8000"

# Page config
st.set_page_config(
    page_title="Book Chatbot",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Book Chatbot")
st.markdown("Upload books and ask questions about them!")

# Sidebar for uploading
with st.sidebar:
    st.header("📤 Upload Book")
    
    uploaded_file = st.file_uploader("Choose a PDF", type="pdf")
    
    if uploaded_file and st.button("Upload & Process"):
        with st.spinner("Processing book... This may take a minute..."):
            # Upload to API
            files = {"file": uploaded_file}
            try:
                response = requests.post(f"{API_URL}/upload", files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    st.success(data.get("message", "Success!"))
                    st.rerun()
                else:
                    st.error("Error uploading book")
            except Exception as e:
                st.error(f"Cannot connect to backend: {str(e)}")
                st.info("Make sure the backend is running on port 8000")
    
    st.divider()
    
    # Show available books
    st.header("📚 Your Books")
    
    try:
        response = requests.get(f"{API_URL}/books")
        
        if response.status_code == 200:
            books = response.json().get("books", [])
            
            if len(books) == 0:
                st.info("No books uploaded yet")
            else:
                for book in books:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"📖 {book['name']}")
                        st.caption(f"{book['size_mb']} MB")
                    with col2:
                        if st.button("🗑️", key=book['name']):
                            try:
                                requests.delete(f"{API_URL}/books/{book['name']}")
                                st.rerun()
                            except:
                                pass
        else:
            st.warning("Cannot load books")
    except:
        st.warning("Backend not running")

# Main area
tab1, tab2 = st.tabs(["💬 Ask Questions", "ℹ️ How to Use"])

with tab1:
    st.header("Ask About Your Books")
    
    # Get book list
    try:
        response = requests.get(f"{API_URL}/books")
        books = response.json().get("books", [])
        book_names = [book['name'] for book in books]
    except:
        book_names = []
    
    if len(book_names) == 0:
        st.info("Please upload a book first using the sidebar")
    else:
        # Select book
        selected_book = st.selectbox("Choose a book:", book_names)
        
        # Select question type
        question_type = st.radio(
            "Type of question:",
            ["General Question", "Create Quiz", "Summarize", "Interview Questions"],
            horizontal=True
        )
        
        # Map to API types
        type_map = {
            "General Question": "general",
            "Create Quiz": "quiz",
            "Summarize": "summary",
            "Interview Questions": "interview"
        }
        
        # Question input
        if question_type == "Create Quiz":
            placeholder = "e.g., Create a quiz about Chapter 5"
        elif question_type == "Summarize":
            placeholder = "e.g., Summarize Chapter 3"
        else:
            placeholder = "e.g., What is machine learning?"
        
        question = st.text_area("Your question:", placeholder=placeholder, height=100)
        
        # Ask button
        if st.button("🔍 Ask", type="primary"):
            if not question:
                st.warning("Please enter a question")
            else:
                with st.spinner("Searching and generating answer..."):
                    try:
                        # Call API
                        params = {
                            "book_name": selected_book,
                            "question": question,
                            "prompt_type": type_map[question_type]
                        }
                        
                        response = requests.get(f"{API_URL}/ask", params=params)
                        
                        if response.status_code == 200:
                            data = response.json()
                            
                            # Show answer
                            st.markdown("### Answer")
                            st.write(data.get("answer", "No answer found"))
                            
                            # Show sources
                            sources = data.get("sources", [])
                            if sources:
                                with st.expander(f"📖 Sources ({len(sources)})"):
                                    for source in sources:
                                        st.write(f"- {source}")
                            
                            # Show chunks
                            chunks = data.get("chunks", [])
                            if chunks:
                                with st.expander("🔍 Retrieved Passages"):
                                    for i, chunk in enumerate(chunks, 1):
                                        st.info(f"**Passage {i}:**\n\n{chunk}")
                        else:
                            st.error("Error getting answer")
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                        st.info("Make sure the backend is running on port 8000")

with tab2:
    st.header("How to Use")
    
    st.markdown("""
    ### 📤 Step 1: Upload a Book
    - Use the sidebar to upload PDF files
    - The system will process the book (this takes 1-2 minutes)
    
    ### 💬 Step 2: Ask Questions
    - Select a book from the dropdown
    - Type your question
    - Choose question type:
        - **General**: Ask anything about the book
        - **Quiz**: Generate multiple choice questions
        - **Summary**: Get chapter summaries
        - **Interview**: Generate interview questions
    
    ### 🔍 How It Works
    1. Book is split into small chunks
    2. Each chunk is converted to embeddings
    3. When you ask, similar chunks are found
    4. AI generates answer using those chunks
    
    ### 💡 Example Questions
    - "Explain machine learning"
    - "Who is the main character?"
    - "Summarize Chapter 5"
    - "What are the key concepts in Chapter 3?"
    - "Create a quiz about neural networks"
    """)

# Footer
st.divider()
st.caption("Book Chatbot - Ask anything about your books!")

