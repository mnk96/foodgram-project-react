#  Проект Foodgram

## Описание проекта
Cайтом, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Пользователям сайта также доступен сервис «Список покупок». Он позволяеь создавать список продуктов, которые нужно купить для приготовления выбранных блюд.
Проект доступен по адресу: https://nataska-kittygram.hopto.org
### Админка: 
логин: vpupkin@yandex.ru
пароль: Qwerty79

![example workflow](https://github.com/mnk96/kittygram_final/actions/workflows/main.yml/badge.svg?event=push)

## Стек технологий:
____
* Python 3.10.12
* Node.js
* Django
* React
* Gunicorn
* Ngnix
* Docker

## Как запустить проект:
____
Команды указаны для Linux.
1. Клонировать репозиторий и перейти в него в командной строке:
```sh
git clone git@github.com:mnk96/foodgram-project-react.git
```
2. Создайте файл .env, в корне проекта
Содержимое .env должно соответствовать примеру:
```sh
POSTGRES_USER=django_user
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_DB=django
DB_HOST=db
DB_PORT=5432
SECRET_KEY=
DEBUG=
ALLOWED_HOSTS=
```
3. Перейдите в папку infra/
```sh
cd infra
```
4. Запустите Docker Compose
```sh
docker compose -f docker-compose.production.yml up 
```
5. Выполните миграции, соберите статические файлы бэкенда и скопируйте их в /backend_static/
```sh
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/static/. /backend_static/
```
6. Проверьте, что страница доступна
```sh
http://localhost/
```
7. Документация доступна по адресу
```sh
http://localhost/api/docs/
```

## Автоматизация деплоя: CI/CD

1. Создайте секреты в GitHub Actions
```sh
DOCKER_USERNAME - логин для Docker Hub
DOCKER_PASSWORD - пароль для Docker Hub
SSH_KEY - закрытый SSH-ключ для доступа к серверу
SSH_PASSPHRASE - passphrase для этого ключа
USER - имя пользователя
HOST - IP-адрес вашего сервера
```

3. Запустите workflow
```sh
Dev/foodgram-project-react$ git add .
Dev/foodgram-project-react$ git commit -m 'Add Actions'
Dev/foodgram-project-react$ git push 
```
## Автор проекта:
Мищенко Наталья