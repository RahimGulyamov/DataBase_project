CREATE SCHEMA IF NOT EXISTS trucking;


CREATE TABLE IF NOT EXISTS trucking.car_models
(
    model    VARCHAR NOT NULL UNIQUE PRIMARY KEY,
    capacity INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS trucking.car
(
    car_number VARCHAR NOT NULL PRIMARY KEY,
    distance   INTEGER,
    model      VARCHAR NOT NULL,
    FOREIGN KEY (model)
        REFERENCES trucking.car_models (model)
);


CREATE TABLE IF NOT EXISTS trucking.driver
(
    driver_id   SERIAL  NOT NULL PRIMARY KEY,
    first_name  VARCHAR NOT NULL,
    last_name   VARCHAR NOT NULL,
    car_number  VARCHAR NOT NULL UNIQUE,
    FOREIGN KEY (car_number)
        REFERENCES trucking.car (car_number),
    driving_exp INTEGER NOT NULL,
    phone_number    NUMERIC NOT NULL UNIQUE,
    payment_account NUMERIC NOT NULL
);


CREATE TABLE IF NOT EXISTS trucking.route
(
    route_id        SERIAL  NOT NULL PRIMARY KEY,
    distance        INTEGER NOT NULL,
    name            VARCHAR,
    drivers_payment INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS trucking.trasportation
(
    transportation_id SERIAL NOT NULL PRIMARY KEY,
    route_id          INTEGER,
    FOREIGN KEY (route_id)
        REFERENCES trucking.route (route_id),
    driver_id         INTEGER,
    FOREIGN KEY (driver_id)
        REFERENCES trucking.driver (driver_id),
    departure_date    TIMESTAMP WITH TIME ZONE,
    arrival_date      TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS trucking.trasportation_history
(
    transportation_id SERIAL                      NOT NULL PRIMARY KEY,
    route_id          INTEGER                     NOT NULL,
    FOREIGN KEY (route_id)
        REFERENCES trucking.route (route_id),
    driver_id         INTEGER                     NOT NULL,
    FOREIGN KEY (driver_id)
        REFERENCES trucking.driver (driver_id),
    departure_date    TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    arrival_date      TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    history_dttm      TIMESTAMP WITHOUT TIME ZONE NOT NULL
);

CREATE TABLE IF NOT EXISTS trucking.client
(
    client_id       SERIAL  NOT NULL PRIMARY KEY,
    first_name      VARCHAR NOT NULL,
    last_name       VARCHAR NOT NULL,
    address         VARCHAR,
    phone_number    NUMERIC NOT NULL UNIQUE,
    payment_account NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS trucking.type_of_goods
(
    type_id SERIAL NOT NULL PRIMARY KEY,
    type    VARCHAR,
    weight  INTEGER
);

CREATE TABLE IF NOT EXISTS trucking.order
(
    order_id          SERIAL  NOT NULL PRIMARY KEY,
    client_id         INTEGER,
    FOREIGN KEY (client_id)
        REFERENCES trucking.client (client_id),
    transportation_id INTEGER,
    FOREIGN KEY (transportation_id)
        REFERENCES trucking.trasportation (transportation_id),
    price             INTEGER NOT NULL,
    type_id           INTEGER,
    FOREIGN KEY (type_id)
        REFERENCES trucking.type_of_goods (type_id)
);

CREATE TABLE IF NOT EXISTS trucking.order_history
(
    order_id          SERIAL                      NOT NULL PRIMARY KEY,
    client_id         INTEGER,
    FOREIGN KEY (client_id)
        REFERENCES trucking.client (client_id),
    transportation_id INTEGER,
    FOREIGN KEY (transportation_id)
        REFERENCES trucking.trasportation_history (transportation_id),
    price             INTEGER                     NOT NULL,
    type_id           INTEGER,
    FOREIGN KEY (type_id)
        REFERENCES trucking.type_of_goods (type_id),
    history_dttm      TIMESTAMP WITHOUT TIME ZONE NOT NULL
);