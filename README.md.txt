# Django Task Manager API

A RESTful Task Management System built using Django and Django REST Framework.

---

## ✅ Features
- Add Task (`POST /api/tasks/`)
- List Tasks (`GET /api/tasks/`)
- Edit Task (`PATCH /api/tasks/{id}/`)
- Delete Task (`DELETE /api/tasks/{id}/`)
- Search by Title: `?search=keyword`
- Search by Date: `?search_date=YYYY-MM-DD`
- Sort by Date: `?sort_by_date=true`

---

## ▶️ How to Run This Project

```bash
# Clone the repo (if needed)
git clone https://gitlab.com/sumadurgatalapaneni/django-tasks-assignment.git

# Go into the project folder
cd myproject

# Create and activate virtual environment
python -m venv env
env\Scripts\activate

# Install requirements
pip install django djangorestframework

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start the server
python manage.py runserver

---

## 📂 Code Structure

- `models.py` → Defines the Task model
- `serializers.py` → Converts Task to JSON
- `views.py` → Contains logic for CRUD + filtering
- `urls.py` → Maps all routes to views

---

## 🧪 Testing

You can test the API using Django REST Framework’s built-in browser UI:
- Add a task
- View task list
- Edit or delete tasks
- Use filters with query params

---

## 🙋 Author

**Thalapaneni Suma Durga**  
Final Year B.Tech, CSE  
Narasaraopeta Engineering College  
