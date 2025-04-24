# Django Tasks Assignment

A RESTful API for task management built with Django REST Framework.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
  - [Local Setup](#local-setup)
  - [Docker Setup](#docker-setup)
- [API Documentation](#api-documentation)
  - [Endpoints](#endpoints)
  - [Models](#models)
  - [Serializers](#serializers)
  - [Viewsets](#viewsets)

## Features
- Create, read, update, and delete tasks
- Filter tasks by completion status
- Search tasks by title
- Filter tasks by creation date
- Sort tasks by creation date
- Pagination support

## Requirements
- Python 3.12+
- Django 4.2.1
- Django REST Framework 3.14.0
- PostgreSQL

## Setup

### Local Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd django-tasks-assignment
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://postgres:postgres@localhost:5432/postgres
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

### Docker Setup

1. Make sure Docker and Docker Compose are installed on your system.

2. Build and start the containers:
```bash
docker-compose up --build
```

3. The API will be available at `http://localhost:80`

## API Documentation

### Endpoints

| Endpoint | Method | Description | URL Name |
|----------|--------|-------------|----------|
| `/tasks/` | GET | List all tasks | task-list |
| `/tasks/` | POST | Create a new task | task-list |
| `/tasks/<id>/` | GET | Retrieve a task | task-detail |
| `/tasks/<id>/` | PUT | Update a task (full update) | task-detail |
| `/tasks/<id>/` | PATCH | Update a task (partial update) | task-detail |
| `/tasks/<id>/` | DELETE | Delete a task | task-detail |
| `/tasks/completed/` | GET | List completed tasks | task-completed |

#### Query Parameters

The task list endpoint (`/tasks/`) supports the following query parameters:

- `search`: Filter tasks by title (case-insensitive)
  - Example: `/tasks/?search=New Task`
- `search_date`: Filter tasks by creation date (format: YYYY-MM-DD)
  - Example: `/tasks/?search_date=2023-04-24`
- `sort_by_date`: Sort tasks by creation date when parameter is present
  - Example: `/tasks/?sort_by_date=true`

### Viewsets

#### TaskView

The `TaskView` viewset handles all CRUD operations for tasks and provides filtering, sorting, and pagination capabilities.

```python
class TaskView(viewsets.ViewSet):
    serializer_class = TaskSerialize
    queryset = Task.objects.all()
```

Available actions:
- `list()`: Get all tasks with optional filtering and pagination
- `create()`: Create a new task
- `retrieve()`: Get a specific task by ID
- `update()`: Update a task (full update)
- `partial_update()`: Update a task (partial update)
- `destroy()`: Delete a task
- `completed()`: Custom action to get all completed tasks
