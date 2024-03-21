# Lizzard Dangeon Master
## Описание
###Суть
Вся суть в том, что огромная куча поверженных ящеров сидит в подвале под Саратовом.
Если они там просто будут сидет, тол взбунтуются и начнется новы виток насилия. 
Но если занять их делом, эксплуатируя рабочую силу, то всем нам будет жить хорошо.

###Идея
Очень много фотографий с большого колличества камер сможет обрабатывая тоьлко очень большая толпа ящеров. 
Чтобы пропускная способность данных оставалась на высоте вне зависимости от колличества набежавших туристов.
Для этого используется ассинхронное программирование и тесно с ним связанный фреймворк fastAPI

###Замысел
Изначанльный замысел был в разделении на модули:
  Запросы обрабатывают отдельные роутеры, которые в свое очередь вызывают методы классов репозиториев.
  по сути в архитектуре этого проекта два слоя. в дальнейшем планируется добавить третий слой сервисов, хоть для 
  подобного пэт проекта достаточно и двух слоев

## Ход разработки
за ходом разработки можно следить на открытой trello [доске](https://trello.com/b/BGPNMSSk/main) по данному проекту 

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
