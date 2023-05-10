CREATE INDEX IF NOT EXISTS car_model_index ON trucking.car_models (model);

CREATE INDEX IF NOT EXISTS car_index ON trucking.car (car_number);

CREATE INDEX IF NOT EXISTS driver_index ON trucking.driver (driver_id);

CREATE INDEX IF NOT EXISTS transportation_index ON trucking.trasportation (transportation_id);

CREATE INDEX IF NOT EXISTS transportation_history_index ON trucking.trasportation_history (transportation_id);

CREATE INDEX IF NOT EXISTS client_index ON trucking.client (client_id);

CREATE INDEX IF NOT EXISTS order_index ON trucking.order (order_id);

CREATE INDEX IF NOT EXISTS order_history_index ON trucking.order_history (order_id);

CREATE INDEX IF NOT EXISTS route_index ON trucking.route (route_id);

CREATE INDEX IF NOT EXISTS type_index ON trucking.type_of_goods (type_id);