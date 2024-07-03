from src.utils.csv_class import CsvProcessor

if __name__ == '__main__':
    # Passando o path do arquivo
    path = './src/data/exemplo.csv'

    # Filtro
    coluna = str(input("Digite a coluna de interesse para filtrar: "))
    atributo = str(input("Digite o atributo de interesse para filtrar: "))
    processor = CsvProcessor(path)
    processor.carrega_csv()
    print(processor.filtra_por(coluna, atributo))

    # Sub_Filtro
    coluna_02 = str(input("Digite a coluna de interesse para filtrar: "))
    operacao = str(input("Digite o simbolo da operação de interesse: "))
    atributo_02 = str(input("Digite o atributo de interesse para filtrar: "))    
    print(processor.sub_filtro(coluna_02, atributo_02, operacao))