from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database config from environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    completed = db.Column(db.Boolean, default=False)

@app.route('/')
def home():
    return "Task Manager Running 🚀"

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{"id": t.id, "title": t.title, "completed": t.completed} for t in tasks])

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    task = Task(title=data['title'])
    db.session.add(task)
    db.session.commit()
    return jsonify({"message": "Task added"})

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    task.completed = True
    db.session.commit()
    return jsonify({"message": "Task updated"})

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})

if __name__ == '__main__':
    app.run()