
# 📚 Book Chatbot

An AI-powered chatbot that lets you upload PDF books and ask questions about their content. Uses RAG (Retrieval Augmented Generation) to provide accurate answers based on the actual book content.
---
## Features

- **Upload PDF Books** - Upload any PDF book for processing
- **Ask Questions** - Ask anything about the book content
- **Quiz Generation** - Create quizzes from any chapter
- **Summarization** - Get summaries of chapters or topics
- **Interview Questions** - Generate interview questions from content
- **Source Tracking** - See which pages answers come from
- **Smart Search** - Finds relevant passages using embeddings
- **Fast Response** - Quick answers using FAISS vector search
---

## Tech Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Vector Database**: FAISS
- **Embeddings**: HuggingFace (all-MiniLM-L6-v2)
- **LLM**: Google FLAN-T5 (can be changed)
- **PDF Processing**: PyPDF
- **Framework**: LangChain

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 4GB RAM minimum (8GB recommended)
- Internet connection (first run downloads models)
---
## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/vedpokharkar495-sudo/book-chatbot.git
cd book-chatbot

# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```
---
### 2. Install Dependencies

```bash
pip install -r requirements.txt
```
---
### 3. Run the Application

```bash
python run.py
```
---
### 4. Open in Browser

- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
---
## Usage Guide

### Step 1: Upload a Book
1. Open the web interface at `http://localhost:8501`
2. Use the sidebar to upload a PDF book
3. Wait for processing to complete (1-2 minutes depending on book size)

### Step 2: Ask Questions
1. Select your book from the dropdown
2. Type your question
3. Choose question type:
   - **General Question**: Ask anything about the book
   - **Create Quiz**: Generate multiple choice questions
   - **Summarize**: Get chapter or topic summaries
   - **Interview Questions**: Generate technical interview questions

### Step 3: View Results
- Read the AI-generated answer
- Expand "Sources" to see which pages were used
- Expand "Retrieved Passages" to see the actual text chunks

## Example Questions

### General Questions
```
- What is machine learning?
- Who is the main character?
- Explain the concept of neural networks
- What are the key takeaways from Chapter 3?
- How does the author define deep learning?
```

### Summarization
```
- Summarize Chapter 5
- Give me an overview of Part 2
- Summarize the introduction
```

### Quiz Generation
```
- Create a quiz from Chapter 10
- Generate 5 questions about neural networks
- Make a quiz about the key concepts in this book
```

### Interview Questions
```
- Give me interview questions from Chapter 7
- What questions might be asked about this topic?
- Create technical interview questions from this book
```
---
## Project Structure

```
book-chatbot/
│
├── config.py              # Configuration settings
├── loader.py              # PDF loading functions
├── splitter.py            # Text splitting functions
├── embeddings.py          # Embedding generation
├── vector_store.py        # FAISS vector storage
├── rag.py                 # RAG pipeline logic
├── backend.py             # FastAPI server
├── frontend.py            # Streamlit UI
├── run.py                 # Start script
├── test.py                # Test script
├── requirements.txt       # Dependencies
├── README.md              # Documentation
│
├── uploads/               # Uploaded PDFs (auto-created)
└── vector_db/             # FAISS indexes (auto-created)
```
---
## Configuration

You can modify settings in `config.py`:

```python
# Change chunk size for splitting
CHUNK_SIZE = 1000          # Characters per chunk
CHUNK_OVERLAP = 200        # Overlap between chunks

# Change number of retrieved chunks
TOP_K_RESULTS = 4          # Number of chunks to search

# Change models
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL_NAME = "google/flan-t5-base"
```
---
### Using Different Models

**For better embeddings:**
```python
EMBEDDING_MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
```

**For better answers (requires GPU):**
```python
LLM_MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"
```

**For faster answers on CPU:**
```python
LLM_MODEL_NAME = "google/flan-t5-small"
```
---
## Testing

Run the test script to verify everything works:

```bash
python test.py
```

This will:
- Check if the API is running
- List available books
- Test asking a question
---
## Troubleshooting

### Common Issues

**1. "Cannot connect to backend"**
- Make sure you ran `python run.py`
- Check if port 8000 is available
- Try accessing http://localhost:8000 directly

**2. "Error processing book"**
- Ensure the PDF is not corrupted
- Check if PDF is password protected
- Try with a smaller PDF first

**3. Model download issues**
- Check your internet connection
- First run will download models (~500MB)
- Try installing models manually:
  ```bash
  python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
  ```

**4. Memory errors**
- Reduce CHUNK_SIZE in config.py
- Process smaller PDFs first
- Close other applications

**5. Slow processing**
- First run is always slower (model loading)
- Use smaller models for faster processing
- Consider using GPU if available

## Use Cases

- **Students**: Study textbooks interactively
- **Researchers**: Quickly find information in papers
- **Book Clubs**: Discuss and analyze books
- **Interview Prep**: Generate interview questions from technical books
- **Content Creation**: Summarize chapters for notes
- **Self-Learning**: Understand complex topics interactively

---
## Contact

For questions or support:
- Open an issue on GitHub
- Email: vedpokharkar495@gmail.com

## Star This Project

If you find this project helpful, please give it a star! It helps others find it too.

---

- Contributing guidelines

You can customize the contact information, GitHub links, and any other personal details!
