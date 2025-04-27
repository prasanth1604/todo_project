# Task Management API - Django REST Framework

Project Overview:

This project implements a fully functional Task Management REST API using Django REST Framework.
It supports complete CRUD operations (Create, Read, Update, Delete) with clean and professional code structure.
The API follows REST principles, handles edge cases, validates inputs (like date format), 
and returns appropriate HTTP status codes with clear messages for both success and error scenarios.
Includes search, date filtering, and ordering features for enhanced usability.

---

## Features

- **Add** a new task
- **Sort** tasks by date
- **Search** tasks by title
- **Search** tasks by date
- **Edit** a task (partial update allowed)
- **Delete** a task 
- **List** all tasks
- Proper **error messages** for invalid requests (e.g., wrong date format, task not found)

---

## Endpoints Overview

| Method | Endpoint | Description |
|:------:|:--------:|:----------- |
| GET | `/tasks/` | List all tasks with optional search, filter, sort |
| POST | `/tasks/` | Create a new task |
| PATCH | `/tasks/{id}/` | Update (partial) a task |
| DELETE | `/tasks/{id}/` | Delete a task |

---

## How to Use Filters

- **Search by Title:**  
  `/tasks/?search=Meeting`
  
- **Filter by Date (YYYY-MM-DD):**  
  `/tasks/?search_date=2024-04-26`
  
- **Sort by Last Updated Date:**  
  `/tasks/?sort_by_date=true`

You can combine filters also!

Example:  
`/tasks/?search=Meeting&search_date=2024-04-26&sort_by_date=true`

---

## Setup and Installation steps:

Follow the steps below to set up and run the Task Management API locally:

### 1. **Clone the Repository:**
       - Start by cloning the repository to your local machine.

### 2. **Set Up a Virtual Environment:**
        - python -m venv venv
        - venv\Scripts\activate
        - Ensure python version is minimum 3.6
        - Tested in python 3.11.0 - Working Fine

### 3. **Install Required Dependencies**
        - Ensure you are in django-tasks-assignment directory
        - pip install -r requirements.txt

### 4. **Apply Database Migrations:**
        - python manage.py makemigrations
        - python manage.py migrate

### 5. **Run Unit and Integrated testcases: (Optional):**
        - pytest (Using django-test package)
        - Ensure all test cases are successful before running server

### 6. **Run the Server:**
        - python manage.py runserver
        - The API will be accessible at http://127.0.0.1:8000/

### 7. **Import Postman Collection for testing (Optional)**
        - A postman collection file (Internship Assignment.postman_collection) is present in repository
        - Import the file into postman
        - You can directly test CRUD operations from there.

---

## Edge Case Handling

The API is designed to handle various edge cases gracefully to ensure a smooth user experience:

1. **Wrong Date Format:**
   - When the user provides a date in an incorrect format (other than `YYYY-MM-DD`), the API will return a `400 Bad Request` error with a clear message:
     ```
     "Invalid date format. Please use YYYY-MM-DD."
     ```

2. **No Tasks Found for Search Criteria:**
   - If no tasks are found when searching by title or date, the API will respond with a `404 Not Found` status and a meaningful message:
     - For date search: 
       ```
       "No tasks found for date YYYY-MM-DD"
       ```
     - For title search: 
       ```
       "No tasks found for title 'task_title'"
       ```
3. **Empty Request Body for Create/Update:**
   - If a POST or PATCH request is made without any data or with invalid data, the API will respond with a 400 Bad Request status and an appropriate message indicating that required fields are missing or invalid.

4. **Invalid Task ID Format:**
   - If a PATCH or DELETE request is made with an invalid task ID format (e.g., using a non-numeric string instead of a valid integer ID), the API will respond with `400 Bad Request` error with the message:
     ```
       "Invalid task ID format. ID must be numeric."
     ```
5. **Deleting Already Deleted or Non-Existent Task:**
   - If a DELETE request is made for a task that is already deleted or does not exist, the API will respond with `404 Not Found` error with the message:
     ```
     "Task not found or already deleted."
     ```

6. **Invalid Sorting Parameter:**
   - If the sort_by_date query parameter is used with a value other than 'true', the API will respond with `400 Bad Request` error with the message:
     ```
       "Invalid value for sort_by_date. It must be 'true'."
     ```