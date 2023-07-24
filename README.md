# rest-loan
Django REST API for Loan management.

### Config
Add the following environment variables in order to run the server:
- DJANGO_SECRET_KEY
- DB_NAME
- DB_USER
- DB_PASSWORD
- DB_HOST
- DB_PORT

### Usage (debug mode)
- Install project requirements:
    ```
    pip install -r requirements.txt
    ```
  
- Run the server:
    ```
    python manage.py runserver
    ```
- Run the tests:
    ```
    pytest tests/
    ```
