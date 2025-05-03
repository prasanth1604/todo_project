## 🚀 Setup Instructions

Follow these steps to get the application running on your local machine:

### 1. Clone the Repository

### 2. Setup Docker-Desktop on your local machine
```bash
https://docs.docker.com/desktop/
```
Make sure to activate the virtual environment already provided in the repo:

### 3. Check whether docker is running in your machine or not

```bash
docker --version
docker-compose --version
```

### 4. Start the application

```bash
docker-compose up -d --build
docker-compose up -d
```

The application runs at `localhost:8000`

### API Endpoints

* **/tasks/**
    * `GET`: Retrieve a list of all tasks.
    * `POST`: Create a new task.

* **/tasks/\<id>**
    * `PUT` (or `PATCH`): Update an existing task with the specified `id`.
    * `DELETE`: Delete the task with the specified `id`.

### Additional Operations

You can perform the following additional operations by using query parameters with the `/tasks/` endpoint:

* **Sort tasks by date:**
    ```
    /tasks/?sort_by_date=true
    ```

* **Search tasks by creation date:**
    Provide the date in `YYYY-MM-DD` format.
    ```
    /tasks/?search_date=2025-05-03
    ```
    This will return all tasks created on May 3rd, 2025.

* **Search tasks by name (partial match):**
    Replace spaces in the search term with `%20`.
    ```
    /tasks/?search=play%20cricket
    ```
    This will return tasks with names containing "play cricket".
