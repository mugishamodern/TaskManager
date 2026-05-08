from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database config - SQLite for simplicity
database_path = os.path.join(os.path.dirname(__file__), 'tasks.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        tasks = Task.query.all()
        return jsonify([{"id": t.id, "title": t.title, "completed": t.completed} for t in tasks]), 200
    except Exception as e:
        logger.error(f"Error fetching tasks: {str(e)}")
        return {"error": "Failed to fetch tasks"}, 500

@app.route('/tasks', methods=['POST'])
def add_task():
    try:
        data = request.json
        
        if not data or 'title' not in data:
            return {"error": "Title is required"}, 400
        
        if not data['title'].strip():
            return {"error": "Title cannot be empty"}, 400
            
        task = Task(title=data['title'])
        db.session.add(task)
        db.session.commit()
        return {"message": "Task added", "id": task.id}, 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding task: {str(e)}")
        return {"error": "Failed to add task"}, 500

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    try:
        task = Task.query.get(id)
        if not task:
            return {"error": "Task not found"}, 404
        
        task.completed = True
        db.session.commit()
        return {"message": "Task updated"}, 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating task: {str(e)}")
        return {"error": "Failed to update task"}, 500

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    try:
        task = Task.query.get(id)
        if not task:
            return {"error": "Task not found"}, 404
        
        db.session.delete(task)
        db.session.commit()
        return {"message": "Task deleted"}, 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting task: {str(e)}")
        return {"error": "Failed to delete task"}, 500

@app.errorhandler(404)
def not_found(error):
    return {"error": "Endpoint not found"}, 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return {"error": "Internal server error"}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=False)