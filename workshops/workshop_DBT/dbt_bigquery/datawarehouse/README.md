# Observações Gerais do projeto: 

### Macros
A macro "generate_schema_name.sql" gera os nomes de schema baseado nos nomes que você for setando durante o seu projeto, sem compromoter as variáveis já setadas no "cliente" do serviço do DBT.

É possível criar/desenvolver qualquer função e chama-la. Basta criar uma Macro e depois, dentro do código SQL, chamar passando a coluna que queira transformar. 