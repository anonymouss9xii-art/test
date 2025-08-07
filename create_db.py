import sqlite3

# الاتصال بقاعدة البيانات (إذا لم تكن موجودة، سيتم إنشاؤها)
conn = sqlite3.connect('exam_results.db')  # اسم قاعدة البيانات
cursor = conn.cursor()

# إنشاء الجدول
cursor.execute('''
CREATE TABLE IF NOT EXISTS exam_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_name TEXT NOT NULL,
    supervisor_name TEXT NOT NULL,
    score INTEGER,
    total INTEGER,
    duration INTEGER,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
''')

# تأكيد التغييرات
conn.commit()

# غلق الاتصال
conn.close()

print("# done coool!")
