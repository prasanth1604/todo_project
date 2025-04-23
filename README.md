# ✅ Django Task Management System API

This is a **RESTful Task Management System** built with **Django** and **Django REST Framework** for the Aereo internship assignment.

It allows users to perform full **CRUD operations** on tasks with filtering, sorting, and search functionality.



## 📦 Setup & Run Instructions

Follow these steps to set up the project on your local machine:

### 1. Clone the repository

Fork and clone the repository:


git clone https://gitlab.com/Sairam-Panuku/django-tasks-assignment.git

cd django-tasks-assignment

2. Create and activate a virtual environment 
bash
Copy code
python -m venv .venv
.venv\Scripts\activate     # On Windows

3. Install dependencies

pip install -r requirements.txt
If requirements.txt is not present, install manually:


pip install django djangorestframework

4. Apply migrations

python manage.py makemigrations
python manage.py migrate

5. Run the server
 code
python manage.py runserver
Now open your browser and go to:
http://127.0.0.1:8000/

🔁 API Endpoints 

Method	Endpoint	            Description
POST	/tasks/	              Add a new task
GET	/tasks/	List all tasks
GET	/tasks/?sort_by_date=true	Sort tasks by creation date
GET	/tasks/?search_date=YYYY-MM-DD	Search tasks by specific date
GET	/tasks/?search=some_title	Search tasks by title
PATCH	/tasks/<id>/update_task/	Partially update a task
DELETE	/tasks/<id>/	Delete a task by ID


📁 App Structure

django-tasks-assignment/
├── core/
│   ├── settings.py
│   └── urls.py          # Main URL configuration
│
├── tasks/
│   ├── models.py        # Task model
│   ├── views.py         # Viewsets for API
│   ├── serializers.py   # Serializers for validation
│   ├── urls.py          # API routes
│   └── tests.py         # API test cases

🧠 Viewset Used

Inside tasks/views.py:

python
Copy code
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        ...
        # Handles sorting and searching logic
This is a ModelViewSet that handles:

list → GET /tasks/

create → POST /tasks/

partial_update → PATCH /tasks/<id>/update_task/

destroy → DELETE /tasks/<id>/

🧰 Serializer Used

Inside tasks/serializers.py:

python code
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
Validates and converts Task model instances into JSON and vice versa.

🌐 URL Names & Routing

In core/urls.py:

python code
path('api/', include('tasks.urls')),    # Root path for all API routes

In tasks/urls.py:

python code
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
All routes are accessible under /tasks/

example: http://127.0.0.1:8000/tasks/

🧪 Testing the API
You can test the API using Postman or curl.

Example using Postman:
POST http://127.0.0.1:8000/tasks/

Headers: Content-Type: application/json

Body: json

{
  "title": "Learn Django",
  "description": "Complete the internship task"
}
GET http://127.0.0.1:8000/tasks/?search=django

🧪 Running Unit Tests
bash
Copy code
python manage.py test tasks


🙌 Author
Sairam Panuku
Aereo Internship Assignment Submission