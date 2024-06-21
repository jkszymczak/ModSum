from python:latest
expose 8000
copy requirements.txt /home/app/
copy . /home/app
workdir /home/app
run pip install -r requirements.txt
run yes | python manage.py makemigrations
run python manage.py migrate
cmd ["python","manage.py","runserver","0.0.0.0:8000"]
