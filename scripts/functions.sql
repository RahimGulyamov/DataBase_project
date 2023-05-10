-- #1 Функция для получения информации о маршруте по ID заказа.

CREATE OR REPLACE FUNCTION get_route_info_by_order_id(arg_order_id INTEGER)
    RETURNS TABLE
            (
                route_id        INTEGER,
                distance        INTEGER,
                name            VARCHAR,
                drivers_payment INTEGER
            )
AS
$$
BEGIN
    RETURN QUERY
        SELECT r.route_id, r.distance, r.name, r.drivers_payment
        FROM trucking.route r
                 INNER JOIN trucking.trasportation t ON r.route_id = t.route_id
                 INNER JOIN trucking.order o ON t.transportation_id = o.transportation_id
        WHERE o.order_id = arg_order_id;
END;
$$ LANGUAGE plpgsql;


-- #2 Функция для получения списка заказов, которые были выполнены в заданный период времени.

CREATE OR REPLACE FUNCTION get_fulfilled_orders(start_date TIMESTAMP WITHOUT TIME ZONE,
                                                end_date TIMESTAMP WITHOUT TIME ZONE)
    RETURNS TABLE
            (
                order_id    INTEGER,
                client_name VARCHAR,
                order_price INTEGER
            )
AS
$$
BEGIN
    RETURN QUERY
        SELECT o.order_id, (c.first_name || ' ' || c.last_name)::VARCHAR AS client_name, o.price AS order_price
        FROM trucking.order o
                 INNER JOIN trucking.client c ON o.client_id = c.client_id
                 LEFT JOIN trucking.trasportation_history t ON o.transportation_id = t.transportation_id
        WHERE t.departure_date BETWEEN start_date AND end_date;
END;
$$ LANGUAGE plpgsql;
-- #3 Функция для получения информации о водителе и автомобиле по номеру машины.

CREATE OR REPLACE FUNCTION get_driver_and_car_info(arg_car_number VARCHAR)
    RETURNS TABLE
            (
                driver_name         VARCHAR,
                driver_phone_number NUMERIC,
                car_model           VARCHAR,
                car_capacity        INTEGER
            )
AS
$$
BEGIN
    RETURN QUERY
        SELECT (d.first_name || ' ' || d.last_name)::VARCHAR AS driver_name,
               d.phone_number                                AS driver_phone_number,
               cm.model                                      AS car_model,
               cm.capacity                                   AS car_capacity
        FROM trucking.driver d
                 INNER JOIN trucking.car c ON d.car_number = c.car_number
                 INNER JOIN trucking.car_models cm ON c.model = cm.model
        WHERE c.car_number = arg_car_number;
END;
$$ LANGUAGE plpgsql;

-- #4 Функция для получения списка клиентов и количества их заказов.

CREATE OR REPLACE FUNCTION get_clients_with_order_count()
    RETURNS TABLE
            (
                client_name VARCHAR,
                order_count BIGINT
            )
AS
$$
BEGIN
    RETURN QUERY
        SELECT (c.first_name || ' ' || c.last_name)::VARCHAR AS client_name, COUNT(o.order_id) AS order_count
        FROM trucking.client c
                 INNER JOIN trucking.order o ON c.client_id = o.client_id
        GROUP BY c.client_id;
END;
$$ LANGUAGE plpgsql;