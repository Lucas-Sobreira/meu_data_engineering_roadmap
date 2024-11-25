# dbt-core & bigquery

Objetivos:

1. Configurar bigquery
2. Boas práticas com sqlfluff e pre-commit
3. Ingerindo dados raw com freshness
4. Staging com yml único
5. Revisitando staging para aplicar macros
    - Criando o nosso de conversão de moeda
6. Revisitando raw para aplicar macro de schema
    - Criando o nosso de multiplos schemas
7. Criando nossa tabela calendário
8. Union de tabelas
9. Snapshot e SDC2

# Configuração do Projeto

### 1. Inicializar o Poetry
``` bash: 
poetry init
poetry install 
```

### 2. Instalar Dependências Adicionais
``` bash: 
poetry add dbt-core dbt-bigquery
poetry add --group dev pre-commit sqlfluff
```

### Configurando o Projeto com Pre-commit e SQLFluff

<p align="justify">Neste projeto, vamos usar **pre-commit** para garantir que nosso código SQL e configuração estejam em conformidade com as melhores práticas antes de cada commit. Também usaremos **SQLFluff** para aplicar regras de formatação específicas ao nosso código SQL.</p>

### Passos para Configuração

1. **Instalar Pre-commit e SQLFluff**
2. **Configurar Pre-commit**
3. **Configurar SQLFluff**

### 1. Instalar Pre-commit e SQLFluff

Primeiro, instale as ferramentas necessárias usando `poetry`:

```bash
poetry add --group dev pre-commit sqlfluff
```

### 2. Configurar Pre-commit

Crie um arquivo `.pre-commit-config.yaml` no diretório raiz do seu projeto com o seguinte conteúdo:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-yaml
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: requirements-txt-fixer
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.3.4
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format
  - repo: https://github.com/sqlfluff/sqlfluff
    rev: 0.11.2
    hooks:
      - id: sqlfluff-lint
      - id: sqlfluff-fix
```

Em seguida, instale os hooks do pre-commit:

```bash
pre-commit install
```

### 3. Configurar SQLFluff

Crie um arquivo `.sqlfluff` no diretório raiz do seu projeto com o seguinte conteúdo:

```ini
[sqlfluff]
templater = dbt
dialect = bigquery
runaway_limit = 10
max_line_length = 80
indent_unit = space

[sqlfluff:templater:dbt]
profiles_dir = .

[sqlfluff:indentation]
tab_space_size = 4

[sqlfluff:layout:type:comma]
spacing_before = touch
line_position = trailing

[sqlfluff:rules:capitalisation.keywords]
capitalisation_policy = lower

[sqlfluff:rules:aliasing.table]
aliasing = explicit

[sqlfluff:rules:aliasing.column]
aliasing = explicit

[sqlfluff:rules:aliasing.expression]
allow_scalar = False

[sqlfluff:rules:capitalisation.identifiers]
extended_capitalisation_policy = lower

[sqlfluff:rules:capitalisation.functions]
capitalisation_policy = lower

[sqlfluff:rules:capitalisation.literals]
capitalisation_policy = lower

[sqlfluff:rules:ambiguous.column_references]  # Number in group by
group_by_and_order_by_style = implicit
```