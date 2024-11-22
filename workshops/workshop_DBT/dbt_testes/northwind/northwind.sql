-- Criação da tabela customers 
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR (255), 
    email VARCHAR (255)
);

-- Inserção de dados na tabela customers com valores nulos e duplicados
INSERT INTO customers (name, email) VALUES 
('Alice', 'alice@example.com'), 
('Bob', Null), 
(Null, 'charlie@example.com'),
('Charlie', 'alice@example.com');

-- Criação da tabela orders
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY, 
    order_date DATE, 
    customer_id INT, 
    status VARCHAR(50), 
    amount DECIMAL (10,2), 
    country_code CHAR(2)
);

-- Inserção de dados na tabela orders com valores nulos e status inválido
INSERT INTO orders (order_date, customer_id, status, amount, country_code) VALUES
('2023-01-01', 1, 'placed', 100.00, 'US'),
('2024-01-02', 2, 'invalid_status', 200.00, 'CA'), -- Status inválido
(Null, 3, 'completed', 300.00, 'GB'), -- Data do pedido nula
('2024-01-04', 4, 'returned', 150.00, Null); -- código do pais nulo

-- Criação da tabela order_items
CREATE TABLE order_items (
    item_id SERIAL PRIMARY KEY, 
    order_id INT, 
    product_id INT, 
    quantity INT, 
    price DECIMAL (10,2)
)

-- Inserção de dados na tabela order_items com order_id sem correspodência em orders
INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
(1, 101, 1, 100.00),
(5, 102, 2, 100.00), -- order_id inexistente
(3, 103, 3, 100.00),
(4, 101, 1, 150.00)