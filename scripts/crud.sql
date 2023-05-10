-- 1. INSERT запрос для таблицы trucking.car
INSERT INTO trucking.car
VALUES ('A777AA', 0, 'International GW3 9800');

-- 2. SELECT запрос для таблицы trucking.order_history
SELECT order_id, price, history_dttm
FROM trucking.order_history
WHERE price > 500;

-- 3. UPDATE запрос для таблицы trucking.transportation
UPDATE trucking.trasportation
SET departure_date = '2023-04-17 10:15:00',
    arrival_date   = '2023-04-19 12:15:00'
WHERE transportation_id = 3;

-- 4. DELETE запрос для таблицы trucking.driver
DELETE
FROM trucking.car
WHERE car_number = 'A777AA';


-- 5. CRUD запросы для таблицы competition:

-- CREATE
INSERT INTO trucking.car
VALUES ('M009AM', 200000, 'Peterbilt 379');

-- READ
SELECT transportation_id, route_id, driver_id
FROM trucking.trasportation_history
LIMIT 5;

-- UPDATE
UPDATE trucking.car_models
SET capacity = 23000
WHERE model = 'Peterbilt 379';

-- DELETE
DELETE
FROM trucking.car
WHERE car_number = 'M009AM';

-- 9. SELECT, который выводит информацию о всех заказах, включая информацию о клиентах и типах грузов:
SELECT o.order_id, o.price, c.first_name, c.last_name, t.type
FROM trucking.order o
         JOIN trucking.client c ON o.client_id = c.client_id
         JOIN trucking.type_of_goods t ON o.type_id = t.type_id;

-- 10. SELECT, который выводит информацию о водителях и количестве их рейсов:
SELECT d.first_name, d.last_name, COUNT(t.transportation_id) as number_of_trips
FROM trucking.driver d
         LEFT JOIN trucking.trasportation t ON d.driver_id = t.driver_id
GROUP BY d.driver_id;

-- 11. SELECT, который выводит информацию о маршрутах, на которых не было совершено ни одной доставки:
SELECT r.name
FROM trucking.route r
         LEFT JOIN trucking.trasportation t ON r.route_id = t.route_id
WHERE t.transportation_id IS NULL;

-- 12. SELECT, который выводит информацию о количестве заказов, сделанных каждым клиентом, и общей сумме их заказов:
SELECT c.first_name, c.last_name, COUNT(o.order_id) as number_of_orders, SUM(o.price) as total_price
FROM trucking.client c
         LEFT JOIN trucking.order o ON c.client_id = o.client_id
GROUP BY c.client_id;
