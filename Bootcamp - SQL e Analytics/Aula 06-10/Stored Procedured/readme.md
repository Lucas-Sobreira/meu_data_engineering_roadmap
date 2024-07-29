## Criação das tabelas - clients e transactions

```sql
CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY NOT NULL,
    limite INTEGER NOT NULL,
    saldo INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY NOT NULL,
    tipo CHAR(1) NOT NULL,
    descricao VARCHAR(10) NOT NULL,
    valor INTEGER NOT NULL,
    cliente_id VARCHAR(100) NOT NULL,
    realizada_em TIMESTAMP NOT NULL DEFAULT NOW()
);
```

## Criação da lógica e Stored Procedure

```sql
CREATE OR REPLACE PROCEDURE realizar_transacao(
    IN p_tipo CHAR(1),
    IN p_descricao VARCHAR(10),
    IN p_valor INTEGER,
    IN p_cliente_id UUID
)

LANGUAGE plpgsql

AS $$

DECLARE
    saldo_atual INTEGER;
    limite_cliente INTEGER;
	saldo_apos_transacao INTEGER;
BEGIN
   SELECT saldo, limite INTO saldo_atual, limite_cliente
   FROM clients
   WHERE id = p_cliente_id;

   RAISE NOTICE 'Saldo atual do cliente: %', saldo_atual;
   RAISE NOTICE 'Limite atual do cliente: %', limite_cliente;

   -- Verifica se a transação é válida com base no saldo e no limite
   IF p_tipo = 'd' AND limite_cliente < saldo_atual - p_valor  THEN
	RAISE EXCEPTION 'Saldo insuficiente para realizar a transação';  
   END IF;

   UPDATE clients
   SET saldo = saldo + CASE WHEN p_tipo = 'd' THEN -p_valor ELSE p_valor END
   WHERE id = p_cliente_id;
	
   -- Insere uma nova transação
   INSERT INTO transactions (tipo, descricao, valor, cliente_id)
   VALUES (p_tipo, p_descricao, p_valor, p_cliente_id);

   SELECT saldo INTO saldo_apos_transacao
   FROM clients
   WHERE id = p_cliente_id;

   RAISE NOTICE 'Saldo do cliente após transacao: %', saldo_apos_transacao;
END;
$$;
```

## Testando uma primeira transação

```sql
CALL realizar_transacao('d', 'amarelo', 8000, '7b575c55-f4e6-4986-8dac-a6d697473869')
```
