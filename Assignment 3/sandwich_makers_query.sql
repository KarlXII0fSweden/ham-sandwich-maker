CREATE DATABASE IF NOT EXISTS sandwich_maker;
USE sandwich_maker;

CREATE TABLE IF NOT EXISTS resources (
    item VARCHAR(50) PRIMARY KEY,
    amount INT
);

CREATE TABLE IF NOT EXISTS sandwiches (
    sandwich_size VARCHAR(50) PRIMARY KEY,
    price DECIMAL(5,2)
);

CREATE TABLE IF NOT EXISTS recipes (
    sandwich_size VARCHAR(50),
    item VARCHAR(50),
    amount INT,
    PRIMARY KEY (sandwich_size, item)
);

INSERT INTO resources (item, amount)
VALUES
    ('bread', 12),
    ('ham', 18),
    ('cheese', 24)
ON DUPLICATE KEY UPDATE amount = VALUES(amount);

INSERT INTO sandwiches (sandwich_size, price)
VALUES
    ('small', 1.75),
    ('medium', 3.25),
    ('large', 5.50)
ON DUPLICATE KEY UPDATE price = VALUES(price);

INSERT INTO recipes (sandwich_size, item, amount)
VALUES
    ('small', 'bread', 2),
    ('small', 'ham', 4),
    ('small', 'cheese', 4),
    ('medium', 'bread', 4),
    ('medium', 'ham', 6),
    ('medium', 'cheese', 8),
    ('large', 'bread', 6),
    ('large', 'ham', 8),
    ('large', 'cheese', 12)
ON DUPLICATE KEY UPDATE amount = VALUES(amount);

SELECT * FROM resources;
SELECT * FROM sandwiches;
SELECT * FROM recipes;