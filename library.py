import streamlit as st
import sqlite3
import os

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect("books.db")
    conn.row_factory = sqlite3.Row  # Enables dictionary-like access to rows
    return conn

# Function to fetch all books from the database
def get_books():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return books

# Function to add a new book to the database
def add_book(title, author, description, file_path):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, description, file_path) VALUES (?, ?, ?, ?)", 
                   (title, author, description, file_path))
    conn.commit()
    conn.close()

# Function to fetch a single book by ID
def get_book_by_id(book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id=?", (book_id,))
    book = cursor.fetchone()
    conn.close()
    return book

# Streamlit UI
st.set_page_config(page_title="My Online Library", page_icon="📚", layout="wide")

# Check if a specific book is selected
query_params = st.query_params
selected_book_id = query_params.get("book_id", None)

# **Book Details Page** (if a book is selected)
if selected_book_id:
    book = get_book_by_id(selected_book_id)
    
    if book:
        st.title(f"📖 {book['title']}")
        st.write(f"✍️ Author: {book['author']}")
        st.write(f"📌 {book['description']}")
        
        with open(book["file_path"], "rb") as file:
            st.download_button(label="📥 Download Book", data=file, file_name=book["title"] + ".pdf")
        
        if st.button("🔙 Back to Library"):
            st.query_params.clear()  # Clears the query parameters
    else:
        st.error("⚠️ Book not found.")
    
    st.stop()  # Stops execution to prevent showing the main page

# **Main Library Page**
st.title("📚 My Online Library")

# Search Bar
search_query = st.text_input("🔍 Search for a book by title or author", "").lower()

# Fetch books
books = get_books()

# Filter books based on search query
if search_query:
    books = [book for book in books if search_query in book["title"].lower() or search_query in book["author"].lower()]

# Display Books as Cards
st.subheader("📖 Available Books")

cols = st.columns(3)  # Creates 3 columns for book cards

for index, book in enumerate(books):
    with cols[index % 3]:  # Distributes books across the columns
        st.markdown(f"### {book['title']}")
        st.write(f"✍️ {book['author']}")
        
        # "Read More" button to open book details
        if st.button("📖 Read More", key=f"book_{book['id']}"):
            st.query_params["book_id"] = book["id"]
            st.rerun()
            
        st.divider()  # Adds a separator between books

# Section to Add New Books
with st.expander("➕ Add a New Book"):
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    description = st.text_area("Description")
    uploaded_file = st.file_uploader("Upload Book (PDF only)", type="pdf")

    if st.button("Add Book"):
        if title and author and uploaded_file:
            file_path = os.path.join("books", uploaded_file.name)
            os.makedirs("books", exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            add_book(title, author, description, file_path)
            st.success(f"✅ '{title}' added successfully!")
            st.rerun()
        else:
            st.error("⚠️ Please provide title, author, and a PDF file.")
