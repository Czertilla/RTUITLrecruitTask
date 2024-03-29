# Lizzard Dangeon Master
## Описание
### Суть
Вся суть в том, что огромная куча поверженных ящеров сидит в подвале под Саратовом.
Если они там просто будут сидеть, то взбунтуются и начнется новы виток насилия. 
Но если занять их делом, эксплуатируя рабочую силу, то всем нам будет жить хорошо.

### Идея
Очень много фотографий с большого колличества камер сможет обрабатывать только очень большая толпа ящеров. 
Чтобы пропускная способность данных оставалась на высоте вне зависимости от колличества набежавших туристов,
 используется ассинхронное программирование и тесно с ним связанный фреймворк FastAPI

### Замысел
Изначанльный замысел был в разделении на слои (как у луковицы):
  Запросы обрабатывают отдельные роутеры, которые в свое очередь вызывают методы классов репозиториев.
  Роутеры ответсвенны только за принятие и валидацию внешних запросов, дальнейшая их обработка в виде т.н.
  бизнеслогики реализована в слое Сервисов. Каждый сервис представляет собой объект класса Сервис, созданный с
  uow (unit if work) параметром, который используется для создания целостных транзакций с базой данных и экономии
  оперативной памяти сервера (uow обеспечивает работу только с необходимыми для конкретного запроса репозиториями
  базы данных, а не со всеми сразу)
  Сервисы ответсвенны только за бизнес логику а uow за создание ассинхронных сессий, внутри которых по командам и
  входным данным от сервисов с базой данных работают уже Репозитории
  Репозитории с помощью ORM технологий работают с базой данных, выполняя запросы Сервисов внутри соззданных uow сессий
  при чем у репозиториев отсутвует доступ к коммитам и откатам и закрытию этих сессий (максимум используется flush, но
  только с позволения сервисов, что указывается в отдельном дополнительном аргументе) 

## Ход разработки
за ходом разработки можно следить на открытой trello [доске](https://trello.com/b/BGPNMSSk/main) по данному проекту 
Также вы можете посетить другие ветви, чтобы следить за ходом разработки

## инструкция по установке
в понравившейся вам папочке прописываем:
```bash
$ git clone https://github.com/Czertilla/RTUITLrecruitTask.git
```
далее необходимо инициализировать виртуальное окружение
```bash
$ py -m venv .venv
```
далее необходимо инициализировать виртуальное окружение
```bash
$ py -m venv .venv
```
запустите виртуальное окружение (неосредствено файл .venv\Scripts\Activate.ps1) или
```bash
$ .venv\Scripts\Activate.ps1
```
теперь необходимо установить все необходимые библиотеки
```bash
$ pip install -r requirements.txt
```
теперь необходимо создать файл .env и записать туда данные по следующему шаблону
```
DB_HOST = 
DB_PORT = 
DB_NAME = 
DB_USER =
DB_PASS = 
DB_DBMS = 
USERS_SECTRET = 
PASSW_SECTRET =
PYTHONPATH=src;test
```
теперь нужно запустить миграцию базы данных
```bash
$ alembic upgrade head
```
не уверен что aлембик благополучно пройдется по всем ревизиям, для этого пересозал все версии (просмтреть ход миграций можно до коммита realise)
далее в папке utils модуле dblocalrequests.py необходимо раскоментитть все строчки в функции requests кроме последней
это необходимо чтобы создать сохранить в базе данных информацию о структуре метаданных камер и динамически создаться схемы по ним
при каждом запуаске приложения. для этого запустите main.py

теперь остается только запустить uvicorn сервер и адоваться жизни
```bash
$ uvicorn main:app --reload
```
 При интеграции докера все процесс должен заметно упроститься
