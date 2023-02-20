DROP TABLE IF EXISTS urls;
CREATE TABLE urls (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(255),
    created_at TIMESTAMP NOT NULL
);

--INSERT INTO urls (name, created_at) VALUES ('Google.com', '2023-02-20'),
--('Test.org', '2023-02-19');