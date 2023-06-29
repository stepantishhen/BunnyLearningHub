# BunnyLearningHub
Проект в Smart Education Lab ИТИС
# Чтобы запустить:
`git clone https://github.com/stepantishhen/BunnyLearningHub`

`cd BunnyLearningHub/`

`git switch <ваше_имя>`

`pip install -r requirements.txt`

`python manage.py migrate`

`python manage.py loaddata data.json`

`python manage.py runserver`
# Перед коммитом:
`python manage.py dumpdata > data.json`

Проверить добавление файлов, закомитить и запушить

Если добавились зависимости:

`pip freeze > requirements.txt`