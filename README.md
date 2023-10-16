#  Проект Foodgram

## Описание проекта
Cайтом, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Пользователям сайта также доступен сервис «Список покупок». Он позволяеь создавать список продуктов, которые нужно купить для приготовления выбранных блюд.
Проект доступен по адресу: https://nataska-kittygram.hopto.org
### Админка:
логин: admin@ya.tu
пароль: adminadmin135

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
2. Активировать виртуальное окружение.
```sh
# Создаём виртуальное окружение.
python3 -m venv venv
# Активируем виртуальное окружение.
source venv/bin/activate
```
3. Установить зависимости
```sh
pip install -r requirements.txt 
```
4. Выполнить миграции
```sh
python manage.py migrate
```
5. Создать суперпользователя
```sh
python manage.py createsuperuser 
```

## Создание Docker_образов
1. Замените username на ваш логин на DockerHub:
```sh
cd frontend
docker build -t username/kittygram_frontend .
cd ../backend
docker build -t username/kittygram_backend .
cd ../nginx
docker build -t username/kittygram_gateway . 
```
2. Загрузите образы на DockerHub:
```sh
docker push username/foodgram_frontend
docker push username/foodgram_backend
```

## Деплой на сервер

1. Подключитесь к удаленному серверу
```sh
ssh -i путь_до_файла_с_SSH_ключом/название_файла_с_SSH_ключом имя_пользователя@ip_адрес_сервера
```

2. Остановите Gunicorn
```sh
sudo systemctl stop gunicorn_foodgram
```

3. Удалите юнит gunicorn
```sh
sudo rm /etc/systemd/system/gunicorn_foodgram.service 
```

4. Установите Docker Compose на сервер
```sh
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt-get install docker-compose-plugin 
```

5. Скопируйте файл docker-compose.production.yml. в директорию foodgram/
```sh
# 1 вариант
scp -i path_to_SSH/SSH_name docker-compose.production.yml username@server_ip:/home/username/foodgram/docker-compose.production.yml
# 2 вариант
cd foodgram
sudo nano docker-compose.production.yml
# Скопировать в файл содержимое docker-compose.production.yml на GitHub
```

6. Скопируйте файл .env на сервер, в директорию foodgram/
```sh
sudo nano .env
```
Содержимое .env должно соответствовать примеру:
```sh
POSTGRES_USER=django_user
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_DB=django
DB_HOST=db
DB_PORT=5432
```

7. Запустите Docker Compose в режиме демона в папке foodgram/
```sh
sudo docker compose -f docker-compose.production.yml up -d 
```

8. Проверьте наличие запущенных контейнеров
```sh
sudo docker compose -f docker-compose.production.yml ps
```

9. Выполните миграции, соберите статические файлы бэкенда и скопируйте их в /backend_static/static/
```sh
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/static/. /backend_static/
```

10. Перенаправьте запросы в Docker
```sh
sudo nano /etc/nginx/sites-enabled/default
```

11. Измените содердимое файла
```sh
# Всё до этой строки оставляем как было.
    location / {
        proxy_pass http://127.0.0.1:9000;
    }
# Ниже ничего менять не нужно.
```

12. Проверьте конфиг на правильность
```sh
sudo nginx -t 
```

13. Перезагрузите конфиг Nginx
```sh
sudo service nginx reload 
```

## Автоматизация деплоя: CI/CD

1. Создайте в папке foodgram/ директорию .github/workflows, а в ней — файл main.yml

2. Скопируйте в этой файл содержимое файла foodgram_workflow.yml

3. Создайте секреты в GitHub Actions
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
Dev/foodgram-project-react_final$ git add .
Dev/foodgram-project-reac_final$ git commit -m 'Add Actions'
Dev/foodgram-project-reac_final$ git push 
```
## Автор проекта:
Мищенко Наталья
