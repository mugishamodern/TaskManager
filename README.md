# Task Manager API

A simple Flask-based REST API for managing tasks with SQLite database backend.

## Prerequisites

- Python 3.11+
- pip

## Setup

1. **Clone the repository**
```bash
git clone <repo-url>
cd TaskManager
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

- `GET /` - Health check
- `GET /tasks` - List all tasks
- `POST /tasks` - Create a new task
  - Body: `{"title": "Task title"}`
- `PUT /tasks/<id>` - Mark task as completed
- `DELETE /tasks/<id>` - Delete a task

## Deployment

### Local Server
```bash
python app.py
```

### Heroku
```bash
heroku create your-app-name
git push heroku main
```

### Docker
```bash
docker build -t taskmanager .
docker run -p 5000:5000 taskmanager
```

### Traditional Server
```bash
gunicorn --bind 0.0.0.0:5000 app:app
```

## Environment Variables

- `PORT` - Server port (default: 5000)
- `FLASK_ENV` - Environment mode (production/development)

**Note:** SQLite database is created automatically in `tasks.db`

## Development

For development, you can run with debug mode:
```bash
FLASK_ENV=development python app.py
```

## License

MIT
