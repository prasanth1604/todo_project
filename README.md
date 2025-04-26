
## Table of Contents

-   [Technology Used](#technology-used)
-   [How to Run Locally](#how-to-run-locally)
    -   [Clone from GitHub](#clone-from-github)
-   [API Details](#api-details)

## Technology Used

-   **Frontend:** HTML5, CSS3, Bootstrap5, JavaScript
-   **Backend:** Python=3.11.4, Django=4.2.5
-   **Database:** PostgreSQL, (Hosted on Render for Production)

## How to Run Locally

### Clone from GitHub

-   Install Python3
-   Install pip

```bash
sudo apt install python3-pip
```

- go to the project directory

-   Create a virtual environment

```bash
python3 -m venv venv
```

-   Activate the virtual environment

windows
`./venv/Scripts/activate`

unix
`source venv/bin/activate`

-   Install the dependencies

```bash
pip3 install -r requirements.txt
```

-   Run the server

```bash
python manage.py runserver
```

-   Open the browser and go to http://127.0.0.1:8000/

-   To deactivate the virtual environment

```bash
deactivate
```

## API DETAILS
- GET /tasks/api - for getting the tasks have certain params ?search for title ?date for search by date, ?sort for sorting date(values can be asc and desc)
- POST /tasks/api - {title,description}
- PATCH /tasks/api/{taskId}
- DELETE /tasks/api/{taskId}
