# Workshop Data Quality com Pydantic e Pandera

[![image](/pic/Doc_TDD.png)](https://lucas-sobreira.github.io/workshop_data_quality/)

Visite a documentação completa: https://lucas-sobreira.github.io/workshop_data_quality/

# Como rodar o código: 

1. Clone o repositório:

```bash
git clone https://github.com/Lucas-Sobreira/workshop_data_quality.git
cd workshop_data_quality
```

2. Configure a versão correta do Python com `pyenv`:

```bash
pyenv install 3.11.5
pyenv local 3.11.5
```

3. Configurar poetry para Python version 3.11.5 e ative o ambiente virtual:

```bash
poetry env use 3.11.5
poetry shell
```

4. Instale as dependencias do projeto:

```bash
poetry install
```

5. Execute os testes para garantir que tudo está funcionando como esperado:

```bash
poetry run task test
```

6. Execute o comando para ver a documentação do projeto:

```bash
poetry run mkdcos serve
```