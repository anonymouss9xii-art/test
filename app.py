from flask import Flask, render_template, request, session, redirect, url_for, jsonify, session
import random, sqlite3, time 
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # ضروري لتفعيل الجلسة
DB_PATH = 'data/exam_results.db'

app.debug = True

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS exam_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_name TEXT,
            supervisor_name TEXT,
            score INTEGER,
            total INTEGER,
            duration INTEGER,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')

init_db()

with open("data/questions.json", encoding="utf-8") as f:
    questions = json.load(f)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/start_exam', methods=['POST'])
def start_exam():
    session['candidate_name'] = request.form['candidate_name']
    session['supervisor_name'] = request.form['supervisor_name']
    session['start_time'] = time.time()

    selected_questions = random.sample(questions, 5)
    session['question_ids'] = [q['id'] for q in selected_questions]

    return render_template('exam.html', questions=selected_questions)

@app.route('/submit', methods=['POST'])
def submit():
    question_ids = session.get('question_ids')
    start_time = session.get('start_time', time.time())

    if not question_ids:
        return redirect(url_for('login'))

    selected_questions = [q for q in questions if q['id'] in question_ids]
    score = 0
    wrong_answers = []

    for q in selected_questions:
        selected = request.form.get(f'q{q["id"]}')
        correct = q['answer']
        if selected is not None and int(selected) == correct:
            score += 1
        else:
            wrong_answers.append({
                'question': q['question'],
                'selected': int(selected) if selected else None,
                'correct': correct,
                'options': q['options']
            })

    duration = int(time.time() - start_time)

    # تخزين النتائج في SQLite
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            INSERT INTO exam_results (candidate_name, supervisor_name, score, total, duration)
            VALUES (?, ?, ?, ?, ?)
        ''', (session.get('candidate_name'), session.get('supervisor_name'), score, len(selected_questions), duration))

    return render_template('result.html',
        score=score,
        total=len(selected_questions),
        correct=score, 
        wrong_answers=wrong_answers,
        candidate=session.get('candidate_name'),
        supervisor=session.get('supervisor_name'),
        duration=duration
    )


# islamco
@app.route("/scenarios")
def show_scenarios():
    # إذا كان scenarios.json داخل مجلد data
    scenarios_path = os.path.join("data", "scenarios.json")
    
    with open(scenarios_path, "r", encoding="utf-8") as f:
        all_scenarios = json.load(f)

    # اختيار 3 سيناريوهات عشوائية
    scenarios = random.sample(all_scenarios, min(3, len(all_scenarios)))

    return render_template("scenarios.html", scenarios=scenarios)


@app.route('/stats')
def stats():
    conn = sqlite3.connect('exam.db') 
    c = conn.cursor()
    c.execute("SELECT candidate_name, supervisor_name, score, duration, submitted_at FROM exam_results ORDER BY submitted_at DESC")
    users = c.fetchall()
    conn.close()

    return render_template('stats.html', users=users)


if __name__ == '__main__':
    from os import getenv
    app.run(host='0.0.0.0', port=int(getenv('PORT', 5000)))





