-- #1 Представление всех клиентов без их адресса и с сокрытием полей номера и счета.
CREATE OR REPLACE VIEW trucking.client_view AS
SELECT client_id,
       first_name,
       last_name,
       CONCAT('*******', substring((phone_number::VARCHAR), 7, 11)) AS masked_phone_number,
       CONCAT(substring(payment_account::VARCHAR, 1, 3), '****',
              substring(payment_account::VARCHAR, 8, 10))           AS masked_payment_account
FROM trucking.client;

-- #2 Представление всех водителей без их адресса и с сокрытием полей номера и счета.
CREATE OR REPLACE VIEW trucking.driver_view AS
SELECT driver_id,
       first_name,
       last_name,
       driving_exp,
       car_number,
       phone_number,
       CONCAT(substring(payment_account::VARCHAR, 1, 3), '****',
              substring(payment_account::VARCHAR, 8, 10)) AS masked_payment_account
FROM trucking.driver;

-- #3 Представление информации о всех текущих заказах, включая информацию о клиентах, типах грузов и времени прибытия:
CREATE OR REPLACE VIEW trucking.order_view AS
SELECT o.order_id, o.price, c.first_name, c.last_name, t.type, tr.arrival_date
FROM trucking.order o
         JOIN trucking.client c ON o.client_id = c.client_id
         JOIN trucking.type_of_goods t ON o.type_id = t.type_id
         JOIN trucking.trasportation tr ON o.transportation_id = tr.transportation_id;

-- #4 Представление статистики клиента
CREATE OR REPLACE VIEW trucking.client_statistic AS
SELECT c.client_id,
       first_name,
       last_name,
       COUNT(o.price) + COUNT(oh.price) AS amount_of_orders,
       SUM(o.price) + SUM(oh.price)     AS total_spent
FROM trucking.client c
         JOIN trucking.order o ON c.client_id = o.client_id
         JOIN trucking.order_history oh ON c.client_id = oh.client_id
GROUP BY c.client_id, first_name, last_name
ORDER BY total_spent DESC, amount_of_orders DESC;

-- #5 Представление статистики финансов по месяцам, по завершившимся транспортировкам
CREATE OR REPLACE VIEW trucking.finance_statistic AS
SELECT DISTINCT DATE_PART('year', th.history_dttm)                                                          AS year,
                DATE_PART('month', th.history_dttm)                                                         AS month,
                SUM(drivers_payment)
                OVER (PARTITION BY DATE_PART('year', th.history_dttm), DATE_PART('month', th.history_dttm)) AS total_payment,
                SUM(price)
                OVER (PARTITION BY DATE_PART('year', th.history_dttm), DATE_PART('month', th.history_dttm)) AS total_price
FROM trucking.trasportation_history th
         JOIN trucking.route r ON th.route_id = r.route_id
         JOIN trucking.order_history oh ON th.transportation_id = oh.transportation_id
ORDER BY total_price DESC, total_payment;

-- #6  Представление для просмотра информации о водителях и машинах, которые они водят:
CREATE OR REPLACE VIEW trucking.driver_car_info AS
    SELECT d.first_name, d.last_name, c.car_number, c.distance, cm.capacity
    FROM trucking.driver d
    JOIN trucking.car c ON d.car_number = c.car_number
    JOIN trucking.car_models cm ON c.model = cm.model;

-- #7 Представление, показывающее информацию о каждом заказе, включая данные о клиенте, машине, маршруте и типе груза:
CREATE OR REPLACE VIEW trucking.order_details AS
    SELECT o.order_id, c.first_name || ' ' || c.last_name AS client_name,
           c2.model AS car_model, r.name AS route_name,
           tg.type AS cargo_type, o.price
    FROM trucking.order o
    JOIN trucking.client c ON o.client_id = c.client_id
    JOIN trucking.trasportation t ON o.transportation_id = t.transportation_id
    JOIN trucking.driver d ON t.driver_id = d.driver_id
    JOIN trucking.car c2 ON d.car_number = c2.car_number
    JOIN trucking.route r ON t.route_id = r.route_id
    JOIN trucking.type_of_goods tg ON o.type_id = tg.type_id;