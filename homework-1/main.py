""" Скрипт для заполнения данными таблиц в БД Postgres. """

import logging
import os

import pandas as pd
import psycopg2
from dotenv import load_dotenv


class NorthDB:
    """Класс для взаимодействия с базой данных"""

    def __init__(self) -> None:
        """Инициализируем данные для подключения к базе данных"""
        load_dotenv()
        self.__dbname = os.getenv("DATABASE")
        self.__user = os.getenv("USER")
        self.__password = os.getenv("PASSWORD")
        self.__host = os.getenv("HOST")
        if os.path.exists("north_data"):
            self.__data_path = "north_data"

    def db_connect(self) -> psycopg2.extensions.connection:
        """
        Метод для подключения к базе данных.

        :return: Коннектор для соединения с базой данных.
        """
        connector = psycopg2.connect(
            dbname=self.__dbname, user=self.__user, password=self.__password, host=self.__host
        )
        return connector

    @staticmethod
    def db_disconnect(connector: psycopg2.extensions.connection) -> None:
        """
        Метод для закрытия соединения с базой данных.

        :param connector: Коннектор соединения с базой данных.
        """
        connector.commit()
        connector.close()

    def insert_data_from_csv(self, filename: str, name_table: str) -> None:
        """
        Метод для вставки данных из CSV-файла в таблицу базы данных.

        :param filename: Название файла CSV.
        :param name_table: Название таблицы в базе данных.
        """
        conn = self.db_connect()
        cur = conn.cursor()
        try:
            file_path = os.path.join(self.__data_path, filename)
            if not os.path.isfile(file_path):
                raise FileNotFoundError("Файл не найден")
            data = pd.read_csv(file_path, encoding="UTF-8", delimiter=",")
            file_columns = ", ".join(data.columns)
            cur.execute(f"SELECT * FROM {name_table}")
            table_columns = ", ".join([column[0] for column in cur.description])
            if file_columns != table_columns:
                raise ValueError("Не совпадают названия столбцов переданного файла и таблицы БД")
            blank_values = "%s, " * len(data.columns)
            insert_query = f"INSERT INTO {name_table} ({file_columns}) VALUES ({blank_values[:-2]})"
            insert_data = [tuple(row) for row in data.values.tolist()]
            cur.executemany(insert_query, insert_data)
        except FileNotFoundError as file_ex:
            logging.error(f"{file_ex.__class__.__name__}: {file_ex}")
        except ValueError as val_ex:
            logging.error(f"{val_ex.__class__.__name__}: {val_ex}")
        except Exception as ex:
            logging.debug(f"{ex.__class__.__name__}: {ex}", exc_info=True)
        else:
            logging.info("Данные успешно загружены")
        finally:
            self.db_disconnect(conn)


def main() -> None:
    """
    Главная функция, создаёт экземпляр класса для работы с базой
    данных и используя метод класса, разносит данные из файлов в БД
    """
    db_north = NorthDB()
    db_north.insert_data_from_csv("employees_data.csv", "employees")
    db_north.insert_data_from_csv("customers_data.csv", "customers")
    db_north.insert_data_from_csv("orders_data.csv", "orders")


if __name__ == "__main__":
    logging.basicConfig(
        filename="db_log.log",
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%d.%m.%Y %H:%M:%S",
        encoding="UTF-8",
    )
    main()
