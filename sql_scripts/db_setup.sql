CREATE DATABASE go_transit;

CREATE USER admin WITH PASSWORD 'password';

GRANT ALL PRIVILEGES ON DATABASE go_transit TO admin;

CREATE TABLE IF NOT EXISTS vehicle_info (
    row_id SERIAL PRIMARY KEY,
    api_timestamp BIGINT NOT NULL,
    vehicle_id INT NOT NULL,
    vehicle_label TEXT NOT NULL,
    latitude NUMERIC(10, 5) NOT NULL,
    longitude NUMERIC(10, 5) NOT NULL,
    trip_id TEXT,
    vehicle_type TEXT,
    "route" TEXT,
    terminal_dest TEXT
);

CREATE TABLE IF NOT EXISTS trip_info (
    row_id SERIAL PRIMARY KEY,
    api_timestamp BIGINT NOT NULL,
    trip_id TEXT,
    route_id TEXT,
    direction TEXT,
    trip_start_time TIME,
    trip_start_date DATE,
    schedule_relationship TEXT,
    stop_id TEXT,
    current_status TEXT
);

CREATE TABLE IF NOT EXISTS stops (
    row_id SERIAL PRIMARY KEY,
    stop_id TEXT,
    stop_name TEXT,
    location_name TEXT,
    latitude NUMERIC(10, 5),
    longitude NUMERIC(10, 5),
    train_station BOOLEAN,
    bus_station BOOLEAN
);

ALTER TABLE stops
ADD CONSTRAINT unique_stop_id UNIQUE (stop_id);

ALTER TABLE trip_info
ADD CONSTRAINT fk_stop_id
FOREIGN KEY (stop_id) REFERENCES stops (stop_id);