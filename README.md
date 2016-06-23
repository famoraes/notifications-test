### To run the project

Create a database on postgres `notific` with user `postgres`
```
    > virtualenv env && source env/bin/activate
    > cd ./src
    > pip install -r requirements.txt
    > ./manage.py migrate
    > ./manage.py runserver
    > ./manage.py createsuperuser
```
