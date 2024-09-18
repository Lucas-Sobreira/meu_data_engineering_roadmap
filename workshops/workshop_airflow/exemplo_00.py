from time import sleep

def primeira_atividade(): 
    print("minha primeira atividade")
    sleep(2)

def segunda_atividade(): 
    print("minha segunda atividade")
    sleep(2)

def terceira_atividade(): 
    print("minha terceira atividade")
    sleep(2)

def pipeline(): 
    primeira_atividade()
    segunda_atividade()
    terceira_atividade()
    print("pipeline terminou")

if __name__ == "__main__": 
    pipeline()