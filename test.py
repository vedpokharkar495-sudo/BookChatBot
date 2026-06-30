


import requests
import time

API = "http://localhost:8000"

def test():
    print("Testing Book Chatbot API...")
    
    # Test home
    r = requests.get(f"{API}/")
    print(f"Home: {r.json()}")
    
    # Test list books
    r = requests.get(f"{API}/books")
    books = r.json().get("books", [])
    print(f"\nBooks available: {len(books)}")
    for book in books:
        print(f"  - {book['name']} ({book['size_mb']} MB)")
    
    # Test ask question
    if len(books) > 0:
        book_name = books[0]['name']
        print(f"\nTesting question on: {book_name}")
        
        r = requests.get(f"{API}/ask", params={
            "book_name": book_name,
            "question": "What is this book about?",
            "prompt_type": "general"
        })
        
        if r.status_code == 200:
            data = r.json()
            print(f"Answer: {data.get('answer', '')[:200]}...")
            print(f"Sources: {data.get('sources', [])}")
        else:
            print(f"Error: {r.text}")
    
    print("\n✅ Test complete!")

if __name__ == "__main__":
    test()


