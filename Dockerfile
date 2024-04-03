from python:bookworm
add . /home/app
workdir /home/app
expose 8000
run pip install -r requirements.txt
run python manage.py makemigrations
run python manage.py migrate
cmd ["python","manage.py","runserver"]
