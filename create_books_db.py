import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("books.db")
cursor = conn.cursor()

# Create the books table
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    description TEXT,
    file_path TEXT NOT NULL
)
""")
cursor.execute("""
DELETE FROM books 
WHERE rowid NOT IN (
    SELECT MIN(rowid) FROM books GROUP BY title, author
)
""")

# Commit changes and close the connection
conn.commit()
conn.close()

print("✅ Database setup complete!")
