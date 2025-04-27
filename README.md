A RESTful Task Management System built using Django and Django REST Framework.
It supports full CRUD operations (Create, Read, Update, Delete) on tasks.

Setup Instructions
1. Clone the Repository
git clone <repository-url>
cd django-tasks-assignment


2. Create and Activate Virtual Environment
python -m venv venv

3. Install Dependencies
pip install -r requirements.txt

4. Apply Migrations
python manage.py makemigrations
python manage.py migrate


5. Run the Development Server
python manage.py runserver

1. Commands
python manage.py runserver: Starts the development server at http://127.0.0.1:8000/.
python manage.py makemigrations: Creates new migrations based on the changes made to models.
python manage.py migrate: Applies migrations to the database.
python manage.py test: Runs tests for the project.