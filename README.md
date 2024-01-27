# Тест-1

* Скопируйте проект к себе на ПК при помощи: git clone https://github.com/ConstCK/Y-Lab-Test-1.git
* 
* Создайте виртуальное окружение (python -m venv venv) и активируйте его (venv\scripts\activate)
* 
* Установите все зависимости при помощи pip install -r requirements.txt в терминале
* 
* Создайте файл .env в каталоге проекта и пропишите в нем настройки БД по примеру .env.example

Примечание: БД должна существовать!

Запустите приложение при помощи (python main.py) из каталога проекта

## Документация:

http://127.0.0.1:8000/docs

http://127.0.0.1:8000/redoc

# НОВОЕ(Тест-2)!!!

* Скопируйте проект к себе на ПК при помощи: git clone https://github.com/ConstCK/Y-Lab-Test-1.git
* 
* **Убедитесь, что Docker (Docker Desktop) установлен и запущен на вашем ПК!!!**

Для запуска приложения в Docker контейнере:

Создайте файл .env в каталоге проекта и пропишите в нем настройки БД по примеру .env.example

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


