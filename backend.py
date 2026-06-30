


from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

import rag
import vector_store as vs

# Create FastAPI app
app = FastAPI(title="Book Chatbot")

# Allow all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
@app.get("/")
def home():
    return {"message": "Book Chatbot API is running! Visit /docs for API documentation."}

@app.post("/upload")
async def upload_book(file: UploadFile = File(...)):
    """
    Upload a PDF book
    """
    # Check if it's a PDF
    if not file.filename.endswith('.pdf'):
        return {"error": "Only PDF files are allowed"}
    
    # Save the file
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    # Process the book
    try:
        book_name = rag.process_book(file_path)
        
        return {
            "message": "Book uploaded and processed successfully!",
            "book_name": book_name,
            "filename": file.filename
        }
    
    except Exception as e:
        return {"error": f"Error processing book: {str(e)}"}

@app.get("/books")
def list_books():
    """
    List all uploaded books
    """
    books = []
    
    if os.path.exists("uploads"):
        for file in os.listdir("uploads"):
            if file.endswith('.pdf'):
                file_path = f"uploads/{file}"
                size = os.path.getsize(file_path) / (1024 * 1024)  # Size in MB
                
                books.append({
                    "name": file.replace('.pdf', ''),
                    "filename": file,
                    "size_mb": round(size, 2)
                })
    
    return {"books": books}

@app.get("/ask")
def ask_question(
    book_name: str,
    question: str,
    prompt_type: str = "general"
):
    """
    Ask a question about a book
    """
    # Check if book exists
    if not os.path.exists(f"uploads/{book_name}.pdf"):
        return {"error": "Book not found"}
    
    # Get answer
    try:
        result = rag.answer_question(book_name, question, prompt_type)
        return result
    except Exception as e:
        return {"error": f"Error answering question: {str(e)}"}

@app.delete("/books/{book_name}")
def delete_book(book_name: str):
    """
    Delete a book and its data
    """
    # Delete PDF
    pdf_path = f"uploads/{book_name}.pdf"
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    
    # Delete vector store
    vs.delete_vector_store(book_name)
    
    return {"message": f"Book '{book_name}' deleted successfully"}

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


