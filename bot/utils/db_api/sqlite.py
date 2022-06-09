import datetime
from decimal import Decimal
import logging
import random
import sqlite3
import time
from loader import logger

# Путь к БД
path_to_db = "data/botBD.sqlite"



def handle_silently(function):
    def wrapped(*args, **kwargs):
        result = None
        try:
            result = function(*args, **kwargs)
        except Exception as e:
            print("{}({}, {}) failed with exception {}".format(
                function.__name__, repr(args[1]), repr(kwargs), repr(e)))
        return result

    return wrapped


####################################################################################################
###################################### ФОРМАТИРОВАНИЕ ЗАПРОСА ######################################
# Форматирование запроса с аргументами
def update_format_with_args(sql, parameters: dict):
    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)
    return sql, tuple(parameters.values())


# Форматирование запроса без аргументов
def get_format_args(sql, parameters: dict):
    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])
    return sql, tuple(parameters.values())

#[REQUESTS]
################################

## USERS
# Получение пользователя
def get_userx(**kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = "SELECT * FROM users WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchone()
    return get_response


# Получение пользователей
def get_usersx(**kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = "SELECT * FROM users WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchall()
    return get_response

# Обновление пользователя
def get_usersx(**kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = "SELECT * FROM users WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchall()
    return get_response

# Добавление пользователя
def add_userx(user_id, user_login, user_name, reg_date):
    with sqlite3.connect(path_to_db) as db:
        db.execute("INSERT INTO users "
                   "(user_id, user_login, user_name, reg_date) "
                   "VALUES (?, ?, ?, ?)",
                   [user_id, user_login, user_name, reg_date])
        db.commit()


# Изменение пользователя
def update_userx(user_id, **kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"UPDATE users SET XXX WHERE user_id = {user_id}"
        sql, parameters = update_format_with_args(sql, kwargs)
        db.execute(sql, parameters)
        db.commit()

# Изменение пользователя
def delete_userx(**kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"DELETE FROM users WHERE "
        sql, parameters = get_format_args(sql, kwargs) 
        db.execute(sql, parameters)
        db.commit()

## zbt_requests
# Получение пользователя
def get_zbt_requestx(**kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = "SELECT * FROM zbt_requests WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchone()
    return get_response


# Получение пользователей
def get_zbt_requestsx(**kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = "SELECT * FROM zbt_requests WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchall()
    return get_response

# Добавление пользователя
def add_zbt_requestx(user_id, user_login, user_name, reg_date):
    with sqlite3.connect(path_to_db) as db:
        db.execute("INSERT INTO zbt_requests "
                   "(user_id, user_login, user_name, reg_date) "
                   "VALUES (?, ?, ?, ?)",
                   [user_id, user_login, user_name, reg_date])
        db.commit()


# Изменение пользователя
def update_zbt_requestx(user_id, **kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"UPDATE zbt_requests SET XXX WHERE user_id = {user_id}"
        sql, parameters = update_format_with_args(sql, kwargs)
        db.execute(sql, parameters)
        db.commit()

# Изменение пользователя
def delete_zbt_requestx(**kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"DELETE FROM zbt_requests WHERE "
        sql, parameters = get_format_args(sql, kwargs) 
        db.execute(sql, parameters)
        db.commit()


#[CREATING TABLES]
################################
all_dbs = 2
def create_bdx():
    with sqlite3.connect(path_to_db) as db:
        # Создание БД с хранением данных пользователей
        check_sql = db.execute("PRAGMA table_info(users)")
        check_sql = check_sql.fetchall()
        check_create_users = [c for c in check_sql]
        if len(check_create_users) == 5:
            logger.info(f"DB was found(1/{all_dbs})")
        else:
            db.execute("CREATE TABLE users("
                       "increment INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "user_id INTEGER, user_login TEXT, user_name TEXT, reg_date TIMESTAMP)")
            logger.info(f"DB was not found(1/{all_dbs}) | Creating...")

        check_sql = db.execute("PRAGMA table_info(zbt_requests)")
        check_sql = check_sql.fetchall()
        check_create_users = [c for c in check_sql]
        if len(check_create_users) == 10:
            logger.info(f"DB was found(2/{all_dbs})")
        else:
            db.execute("CREATE TABLE zbt_requests("
                       "increment INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "user_id INTEGER, user_login TEXT, user_name TEXT, reg_date TIMESTAMP,"
                       "input_name TEXT, input_email TEXT, input_age TEXT, input_about TEXT, input_nickname TEXT)")
            logger.info(f"DB was not found(1/{all_dbs}) | Creating...")