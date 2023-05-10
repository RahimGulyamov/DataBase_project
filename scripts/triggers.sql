-- #1 Триггер, который автоматически обновляет столбец "distance" в таблице "car",
-- когда новая транспортировка добавляется в таблицу "transportation".

CREATE OR REPLACE FUNCTION update_car_distance() RETURNS TRIGGER AS
$$
BEGIN
    UPDATE trucking.car c
    SET distance = c.distance + r.distance
    FROM trucking.route r
    WHERE car_number = (SELECT car_number
                        FROM trucking.driver
                        WHERE driver_id = NEW.driver_id)
      AND r.route_id = NEW.route_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_car_distance_trigger
    AFTER INSERT
    ON trucking.trasportation
    FOR EACH ROW
EXECUTE FUNCTION update_car_distance();

-- #2 Триггер, который автоматически добавляет новую запись в таблицу "trasportation_history",
-- когда транспортировка завершается, и удаляет из таблицы с активными транспортировками.
-- Запись будет содержать информацию о транспортировке,
-- включая дату и время отправления и прибытия.

CREATE OR REPLACE FUNCTION add_transportation_history()
    RETURNS TRIGGER AS
$$
BEGIN
    INSERT INTO trucking.trasportation_history (route_id, driver_id, departure_date, arrival_date, history_dttm)
    VALUES (OLD.route_id, OLD.driver_id, OLD.departure_date, OLD.arrival_date, NOW());
    DELETE
    FROM trucking.trasportation
    WHERE transportation_id = OLD.transportation_id;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER add_transportation_history_trigger
    AFTER UPDATE OF arrival_date
    ON trucking.trasportation
    FOR EACH ROW
EXECUTE FUNCTION add_transportation_history();

-- #3 Триггер, который автоматически добавляет новую запись в таблицу "order_history",
-- когда транспортировка завершается. Запись будет содержать информацию о транспортировке,
-- включая дату и время отправления и прибытия.

CREATE OR REPLACE FUNCTION add_order_history()
    RETURNS TRIGGER AS
$$
BEGIN
    INSERT INTO trucking.order_history (client_id, transportation_id, price, type_id, history_dttm)
    SELECT client_id,
           transportation_id,
           price,
           type_id,
           NOW()
    FROM trucking.order
    WHERE transportation_id = OLD.transportation_id;
    DELETE
    FROM trucking."order"
    WHERE transportation_id = OLD.transportation_id;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER add_order_history_trigger
    AFTER UPDATE OF arrival_date
    ON trucking.trasportation
    FOR EACH ROW
EXECUTE FUNCTION add_order_history();
