import json

import psycopg2

from config import config


def main():
    script_file = 'fill_db.sql'
    json_file = 'suppliers.json'
    db_name = 'my_new_db'

    params = config()
    conn = None

    message = create_database(params, db_name)
    print(message)

    params.update({'dbname': db_name})
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                execute_sql_script(cur, script_file)
                print(f"БД {db_name} успешно заполнена")

                create_suppliers_table(cur)
                print("Таблица suppliers успешно создана")

                suppliers = get_suppliers_data(json_file)
                insert_suppliers_data(cur, suppliers)
                print("Данные в suppliers успешно добавлены")

                add_foreign_keys(cur, json_file)
                print(f"FOREIGN KEY успешно добавлены")

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def create_database(params, db_name) -> str:
    """Создает новую базу данных."""

    message = f"БД {db_name} успешно создана"
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute("SELECT datname FROM pg_database")
        databases = cur.fetchall()
        for db in databases:
            if db_name in db:
                message = f"БД {db_name} уже была создана"
                break
        else:
            cur.execute(f"CREATE DATABASE {db_name}")
    conn.close()
    return message


def execute_sql_script(cur, script_file) -> None:
    """Выполняет скрипт из файла для заполнения БД данными."""

    with open(script_file, encoding="UTF-8") as script:
        cur.execute(script.read())


def create_suppliers_table(cur) -> None:
    """Создает таблицу suppliers."""

    cur.execute("""
    CREATE TABLE IF NOT EXISTS suppliers(
        supplier_id SERIAL PRIMARY KEY,
        company_name VARCHAR(50) NOT NULL,
        contact VARCHAR(150),
        address VARCHAR(150),
        phone VARCHAR(25),
        fax VARCHAR(25),
        homepage TEXT,
        products TEXT[]
        )
    """)


def get_suppliers_data(json_file: str) -> list[dict]:
    """Извлекает данные о поставщиках из JSON-файла и возвращает список словарей с соответствующей информацией."""

    with open(json_file, encoding="UTF-8") as file:
        suppliers_data = json.load(file)
    return suppliers_data


def insert_suppliers_data(cur, suppliers: list[dict]) -> None:
    """Добавляет данные из suppliers в таблицу suppliers."""

    data = (tuple(supplier.values()) for supplier in suppliers)
    cur.executemany("""
        INSERT INTO suppliers (
            company_name,
            contact,
            address,
            phone,
            fax,
            homepage,
            products
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, data)


def add_foreign_keys(cur) -> None:
    """Добавляет foreign key со ссылкой на supplier_id в таблицу products."""

    cur.execute("ALTER TABLE products ADD COLUMN supplier_id INTEGER")
    cur.execute("ALTER TABLE products ADD FOREIGN KEY(supplier_id) REFERENCES suppliers(supplier_id)")


if __name__ == '__main__':
    main()
