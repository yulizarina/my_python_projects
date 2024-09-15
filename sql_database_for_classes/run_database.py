import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('my_classes.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER
)
''')

# Insert data into the table
cursor.execute('''
INSERT INTO students (name, age) VALUES (?, ?)
''', ('John Doe', 25))

# Commit the changes
conn.commit()

# Update data in the table
cursor.execute('''
UPDATE students SET age = ? WHERE id = ?
''', (26, 1))

# Commit the changes
conn.commit()

# Close the connection
conn.close()
