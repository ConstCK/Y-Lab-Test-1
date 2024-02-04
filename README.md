# НОВОЕ(Тест-2)!!!

* Скопируйте проект к себе на ПК при помощи: git clone https://github.com/ConstCK/Y-Lab-Test-1.git
* Перейдите в папку проекта
* В терминале создайте виртуальное окружение (например python -m venv venv) и активируйте его (venv\scripts\activate)
* Установите все зависимости при помощи pip install -r requirements.txt
* Создайте файл .env в каталоге проекта и пропишите в нем настройки БД по примеру .env.example

_**Убедитесь, что Docker (Docker Desktop) установлен и запущен на вашем ПК!!!**_

# Для запуска приложения в Docker контейнере:

## Запуск приложения:

Команда в терминале docker-compose --file app.yaml up -d

## Доступ к приложению:

http://localhost:8000/

## Документация:

http://localhost:8000/docs

http://localhost:8000/redoc

## Доступ к панели администрирования БД:

http://localhost:8888/

Примечания:

Введите данные из .env файла для доступа во все поля кроме сервера, сервер - my_db

## Запуск тестов:

Команда в терминале docker-compose --file tests.yaml up

## Остановка сервисов:

docker-compose --file app.yaml down
docker-compose --file tests.yaml down

## Остановка сервисов с очисткой БД:

docker-compose --file app.yaml down --volumes
docker-compose --file tests.yaml down --volumes
