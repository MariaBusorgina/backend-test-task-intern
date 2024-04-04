## DRF-shop-project
Django проект магазина продуктов.

### Установка
1. Создать и активировать виртуальное окружение 
```bash
python -m venv venv
source venv/bin/activate
```
2. Установить зависимости
```bash
pip install -r requirements.txt
```
3. Перейти в каталог
```bash
cd project
```
4. Создать и применить миграции
```bash
python manage.py makemigrations
python manage.py migrate
```
5. Создать администратора магазина
```bash
python manage.py createsuperuser
```
6. Запуск сервера
```bash
python manage.py runserver
```
7. Добавить категории, подкатегории, продукты через интерфейс администратора (http://127.0.0.1:8000/admin/)

### Функциональные возможности
**Для администратора сайта:**
- создание, редактирование, удаление категорий и подкатегорий товаров;
- добавление, изменение, удаление продуктов.


**Доступные эндпоинты для всех пользователей:**
- POST http://127.0.0.1:8000/api/auth/users/ - регистрация нового пользователя  
Обязательные параметры: username, password


- POST http://127.0.0.1:8000/auth/token/login/ - аутентификация пользователя (получение токена)  
Обязательные параметры: username, password


- GET http://127.0.0.1:8000/api/category/ - просмотр всех категорий с подкатегориями (предусмотрена пагинация);


- GET http://127.0.0.1:8000/api/products/ - просмотр всех продуктов (предусмотрена пагинация);


**Доступные эндпоинты для авторизованных пользователей:**
- POST http://127.0.0.1:8000/api/basket_item/ - добавление товара в корзину (если данный товар уже есть в корзине, изменяем количество);  
Обязательные параметры: id продукта, количество товара  
Пример запроса: Body={"product": 1, "quantity": 2}


- PATCH http://127.0.0.1:8000/api/basket_item/{id_basket_item}/ - изменение количества товара в корзине (если пользователь указывает количество продукта "0" - продукт удаляется из корзины)  
Обязательные параметры: количество товара  
Пример запроса: Body={"quantity": 2}


- GET http://127.0.0.1:8000/api/basket_total/{basket_id}/ - просмотр состава корзины с подсчетом количества товаров и суммы стоимости товаров в корзине;


- DELETE http://127.0.0.1:8000/api/basket_item/{basket_id}/ - полная очистка корзины.


#### Стек:
Python
Django REST Framework
Djoser
