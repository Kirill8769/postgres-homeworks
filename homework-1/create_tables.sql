-- SQL-команды для создания таблиц

CREATE TABLE employees (
	employee_id SERIAL PRIMARY KEY,
	first_name VARCHAR(32) NOT NULL,
	last_name VARCHAR(32) NOT NULL,
	title VARCHAR(128) NOT NULL,
	birth_date VARCHAR(16) NOT NULL,
	notes TEXT NOT NULL
);


CREATE TABLE customers (
	customer_id CHAR(5) PRIMARY KEY,
	company_name VARCHAR(128) NOT NULL,
	contact_name VARCHAR(128) NOT NULL
);


CREATE TABLE orders (
	order_id INT PRIMARY KEY,
	customer_id CHAR(5) REFERENCES customers(customer_id) NOT NULL,
	employee_id INT REFERENCES employees(employee_id) NOT NULL,
	order_date VARCHAR(16) NOT NULL,
	ship_city VARCHAR(32) NOT NULL
);
