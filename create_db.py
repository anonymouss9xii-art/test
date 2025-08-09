import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS exam_results")

c.execute("""
CREATE TABLE IF NOT EXISTS exam_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_name TEXT NOT NULL,
    supervisor_name TEXT NOT NULL,
    score INTEGER,
    total INTEGER,
    duration INTEGER,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("# done coool!")
