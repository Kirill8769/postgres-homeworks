-- Напишите запросы, которые выводят следующую информацию:
-- 1. Название компании заказчика (company_name из табл. customers) и ФИО сотрудника, работающего над заказом этой компании (см таблицу employees),
-- когда и заказчик и сотрудник зарегистрированы в городе London, а доставку заказа ведет компания United Package (company_name в табл shippers)
SELECT
	cust.company_name,
    CONCAT(e.first_name, ' ', e.last_name) AS employee
FROM orders o
	JOIN customers cust USING(customer_id)
	JOIN employees e USING(employee_id)
WHERE
    cust.city = 'London'
    AND e.city = 'London'
    AND o.ship_via = (
        SELECT shipper_id
        FROM shippers
        WHERE company_name = 'United Package'
    )
ORDER BY 1 DESC, 2 DESC;

-- 2. Наименование продукта, количество товара (product_name и units_in_stock в табл products),
-- имя поставщика и его телефон (contact_name и phone в табл suppliers) для таких продуктов,
-- которые не сняты с продажи (поле discontinued) и которых меньше 25 и которые в категориях Dairy Products и Condiments.
-- Отсортировать результат по возрастанию количества оставшегося товара.


-- 3. Список компаний заказчиков (company_name из табл customers), не сделавших ни одного заказа
SELECT company_name
FROM customers
LEFT JOIN orders USING(customer_id)
WHERE order_id IS NULL
ORDER BY company_name;

-- 4. уникальные названия продуктов, которых заказано ровно 10 единиц (количество заказанных единиц см в колонке quantity табл order_details)
-- Этот запрос написать именно с использованием подзапроса.
SELECT product_name
FROM products
WHERE product_id IN (
	SELECT product_id
	FROM order_details
	WHERE quantity = 10);
