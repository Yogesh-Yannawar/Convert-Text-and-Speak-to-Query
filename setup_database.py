import sqlite3

# Create database and table
conn = sqlite3.connect('student.db')
cursor = conn.cursor()

# Create STUDENT table
cursor.execute('''
CREATE TABLE IF NOT EXISTS STUDENT (
    NAME TEXT NOT NULL,
    CLASS TEXT NOT NULL,
    SECTION TEXT NOT NULL,
    MARKS INTEGER NOT NULL
)
''')

# Insert sample data
sample_data = [
    ('John Doe', 'Computer', 'A', 85),
    ('Sarah Smith', 'Computer', 'B', 92),
    ('Mike Johnson', 'Computer', 'A', 78),
    ('Emily Brown', 'Physics', 'A', 88),
    ('David Wilson', 'Physics', 'B', 95),
    ('Lisa Anderson', 'Chemistry', 'A', 82),
    ('Tom Martinez', 'Chemistry', 'B', 76),
    ('Anna Taylor', 'Mathematics', 'A', 91),
    ('James White', 'Mathematics', 'B', 87),
    ('Maria Garcia', 'Computer', 'C', 94),
    ('Robert Lee', 'Physics', 'C', 89),
    ('Jennifer Davis', 'Chemistry', 'C', 83),
    ('William Rodriguez', 'Mathematics', 'C', 90),
    ('Jessica Martinez', 'Computer', 'A', 96),
    ('Michael Brown', 'Physics', 'A', 79),
]

cursor.executemany('INSERT INTO STUDENT VALUES (?, ?, ?, ?)', sample_data)

conn.commit()
print(f"✅ Database created successfully!")
print(f"✅ Inserted {len(sample_data)} sample records")

# Verify data
cursor.execute('SELECT COUNT(*) FROM STUDENT')
count = cursor.fetchone()[0]
print(f"✅ Total records in database: {count}")

# Show sample data
print("\n📊 Sample data:")
cursor.execute('SELECT * FROM STUDENT LIMIT 5')
rows = cursor.fetchall()
for row in rows:
    print(f"   {row}")

conn.close()
print("\n🎉 Setup complete! You can now run the application.")
