
INSERT INTO poi_type(id, name) values (1, 'Station');
ALTER SEQUENCE poi_type_id_seq RESTART WITH 1;


DROP TABLE IF EXISTS csv_stops;
CREATE TABLE csv_stops (
    stop_id                 VARCHAR(255) NOT NULL,
    stop_code               VARCHAR(255),
    stop_name               VARCHAR(255),
    stop_lat                REAL NOT NULL,
    stop_lon                REAL NOT NULL,
    location_type           VARCHAR(255),
    parent_station          VARCHAR(255),
    stop_timezone           VARCHAR(255),
    wheelchair_boarding     SMALLINT,
    platform_code           VARCHAR(255),
    zone_id                 VARCHAR(255),
    CONSTRAINT csv_stops_pkey PRIMARY KEY(stop_id)
);

\COPY csv_stops FROM '/home/cuong/Projects/Amsterdam/mapitout-backend/api/deploy/db/stops.txt' delimiter ',' csv header;
ANALYZE VERBOSE csv_stops;


BEGIN;
INSERT INTO poi (name, description, geo_location, poi_type_id)
SELECT DISTINCT ON (stop_code)
    stop_code,
    stop_name,
    ST_SetSRID(ST_MakePoint(CAST(stop_lon AS FLOAT), CAST(stop_lat AS FLOAT)), 4326),
    1
FROM
    csv_stops
WHERE
    stop_code is not null;
COMMIT;


INSERT INTO poi_type(id, name) values (2, 'School');
ALTER SEQUENCE poi_type_id_seq RESTART WITH 2;