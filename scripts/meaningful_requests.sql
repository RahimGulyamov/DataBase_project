-- #1
-- Этот запрос вернет модели автомобилей (максимум 10) с самым большим средним пробегом,
-- которые в базе данных у более 2 автомобилей (2 - так как пока еще данныз мало в бд).
-- Так можно судить о самых долговечных моделях
SELECT model, AVG(distance) as avg_distance
FROM trucking.car
GROUP BY model
HAVING COUNT(*) >= 2
ORDER BY avg_distance DESC
LIMIT 10;


-- #2
--   Этот запрос вернет список клиентов, у которых общая сумма потраченных денег на заказы превышает 2000,
--   отсортированных по убыванию общей суммы.
SELECT first_name, last_name, SUM(o.price) + SUM(oh.price) as total_spent
FROM trucking.client c
         JOIN trucking.order o ON c.client_id = o.client_id
         JOIN trucking.order_history oh ON c.client_id = oh.client_id
GROUP BY first_name, last_name
HAVING SUM(o.price) + SUM(oh.price) > 2000
ORDER BY total_spent DESC;


-- #3
-- Этот запрос вернет список водителей, отсортированных по пройденной ими дистанции за 2022 год, а также их оплату.
-- Так можно определить лучшего водителя за это время
SELECT DISTINCT d.driver_id,
                first_name,
                last_name,
                SUM(distance) OVER (PARTITION BY d.driver_id)        as total_distance,
                SUM(drivers_payment) OVER (PARTITION BY d.driver_id) as total_payment
FROM trucking.driver d
         JOIN trucking.trasportation_history th ON d.driver_id = th.driver_id
         JOIN trucking.route r ON th.route_id = r.route_id
WHERE DATE_PART('year', th.history_dttm) = 2022
ORDER BY total_distance DESC, total_payment DESC;


-- #4
-- Этот запрос вернет общую оплату водителей и сумму заказов за разные года
SELECT DISTINCT DATE_PART('year', th.history_dttm)                                          AS year,
                SUM(drivers_payment) OVER (PARTITION BY DATE_PART('year', th.history_dttm)) AS total_payment,
                SUM(price) OVER (PARTITION BY DATE_PART('year', th.history_dttm))           AS total_price
FROM trucking.trasportation_history th
         JOIN trucking.route r ON th.route_id = r.route_id
         JOIN trucking.order_history oh ON th.transportation_id = oh.transportation_id
ORDER BY total_price DESC, total_payment;


-- #5
--   Этот запрос вернет имена, фамилии, опыт вождения и ранг первых 10 водителей, отсортированных по рангу.
SELECT first_name,
       last_name,
       driving_exp,
       RANK() OVER (ORDER BY driving_exp DESC) as rank
FROM trucking.driver
ORDER BY rank
LIMIT 10;


-- #6
-- Этот запрос вернет количество транспортировок и суммы заказов для каждого маршрута
SELECT DISTINCT r.route_id,
                name AS route_name,
                COUNT(*) OVER (PARTITION BY r.route_id) AS amount,
                SUM(price) OVER (PARTITION BY r.route_id) AS total_price
FROM trucking.route r
         JOIN trucking.trasportation_history th ON r.route_id = th.route_id
         JOIN trucking.order_history oh ON th.transportation_id = oh.transportation_id
ORDER BY  total_price DESC, amount DESC;