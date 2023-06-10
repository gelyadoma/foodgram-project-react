# API Foodgram 
![example workflow](https://github.com/gelyadoma/foodgram-project-react/actions/workflows/main.yml/badge.svg)

Этот проект позволяет взаимодействовать с сервисом Foodgram через API. Сервис предоставляет возможность публиковать свои рецепты, добавлять в избранные рецепты других авторов и составлять список покупок.
В проекте собранны файлы для развертывания приложения локально и на удаленном сервере в Docker.


## Автор проекта 
- [@gelyadoma](https://github.com/gelyadoma) - Ангелина Доматьева

## Используемые технологии:
- Python
- Django
- Docker
- Dockercompose
- Nginx
- Gunicorn
Более подробно см. 'foodgram\requirements.txt'

## Функционал

- Рецепты на всех страницах **сортируются** по дате публикации (новые — выше)
- Работает **фильтрация** по тегам, в том числе на странице избранного и на странице рецептов одного автора
- Работает **пагинатор** (в том числе при фильтрации по тегам)
- Для **авторизованных** пользователей:
 * Доступна **главная страница**
 * Доступна **страница другого пользователя**
 * Доступна **страница отдельного рецепта**
 * Доступна страница **«Мои подписки»**:
 1. Можно подписаться и отписаться на странице рецепта
 2. Можно подписаться и отписаться на странице автора
 3. При подписке рецепты автора добавляются на страницу «Мои подписки» и удаляются оттуда при отказе от подписки
 * Доступна страница **«Избранное»**:
 1. На странице рецепта есть возможность добавить рецепт в список избранного и удалить его оттуда
 2. На любой странице со списком рецептов есть возможность добавить рецепт в список избранного и удалить его оттуда
 * Доступна страница **«Список покупок»**:
 1. На странице рецепта есть возможность добавить рецепт в список покупок и удалить его оттуда
 2. На любой странице со списком рецептов есть возможность добавить рецепт в список покупок и удалить его оттуда
 3. Есть возможность выгрузить файл (.pdf) с перечнем и количеством необходимых ингредиентов для рецептов из «Списка покупок»
 4. Ингредиенты в выгружаемом списке не повторяются, корректно подсчитывается общее количество для каждого ингредиента
 * Доступна страница **«Создать рецепт»**:
 1. Есть возможность опубликовать свой рецепт
 2. Есть возможность отредактировать и сохранить изменения в своём рецепте
 3. Есть возможность удалить свой рецепт
 * Доступна и работает форма **изменения пароля**
 * Доступна возможность **выйти из системы** (разлогиниться)
- Для **неавторизованных** пользователей:
 * Доступна **главная страница**
 * Доступна **страница отдельного рецепта**
 * Доступна и работает **форма авторизации**
 * Доступна и работает **система восстановления пароля**
 * Доступна и работает **форма регистрации**
- **Администратор** и **админ-зона**:
 * Все модели выведены в админ-зону
 * Для модели пользователей включена **фильтрация** по имени и email
 * Для модели рецептов включена **фильтрация** по названию, автору и тегам
 * На админ-странице рецепта отображается общее число добавлений этого рецепта в избранное
 * Для модели ингредиентов включена **фильтрация** по названию

# URL's

- http://51.250.97.159
- http://51.250.97.159/admin
- http://51.250.97.159/api

# Документация

Для просмотра документации к API перейдите по адресу:
- http://51.250.97ю159/api/redoc


## Установки для развертывания проекта
## Для работы с удаленным сервером (на ubuntu):
* Выполните вход на свой удаленный сервер

* Установите docker на сервер:
```
sudo apt install docker.io 
```
* Установите docker-compose на сервер:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
* Локально отредактируйте файл nginx.conf и в строке server_name впишите свой IP
* Скопируйте файлы docker-compose.yml и nginx.conf из директории infra на сервер:
```
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```
* Cоздайте .env файл и впишите:
    ```
    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<имя базы данных postgres>
    DB_USER=<пользователь бд>
    DB_PASSWORD=<пароль>
    DB_HOST=<db>
    DB_PORT=<5432>
    SECRET_KEY=<секретный ключ проекта django>
    ```
* На сервере соберите docker-compose:
```
sudo docker-compose up -d --build
```
* После успешной сборки на сервере выполните команды (только после первого деплоя):
    - Соберите статические файлы:
    ```
    sudo docker-compose exec backend python manage.py collectstatic --noinput
    ```
    - Примените миграции:
    ```
    sudo docker-compose exec backend python manage.py migrate --noinput
    ```
    - Загрузите ингридиенты  в базу данных (необязательно):  
    ```
    sudo docker-compose exec backend python manage.py load_file_json <Название файла из директории data>
    ```
    - Создать суперпользователя Django:
    ```
    sudo docker-compose exec backend python manage.py createsuperuser
    ```
    - Проект доступен и работоспособен!
