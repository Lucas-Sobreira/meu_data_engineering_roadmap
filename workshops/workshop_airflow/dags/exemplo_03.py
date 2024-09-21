from time import sleep
from airflow.decorators import dag, task
from datetime import datetime   

@dag(
        dag_id="minha_terceira_dag", 
        description="minha etl braba", 
        schedule="* * * * *", #roda todo minuto
        start_date=datetime(2024, 9, 18),
        catchup=False #backfill
)
def pipeline(): 
    @task
    def primeira_atividade(): 
        print("minha primeira atividade")
        sleep(2)

    @task
    def segunda_atividade(): 
        print("minha segunda atividade")
        sleep(2)

    @task
    def terceira_atividade(): 
        print("minha terceira atividade")
        sleep(2)

    @task
    def quarta_atividade(): 
        print("pipeline terminou")
        sleep(2)

    t1 = primeira_atividade()
    t2 = segunda_atividade()
    t3 = terceira_atividade()
    t4 = quarta_atividade()    

    t1.set_downstream([t2, t3])  # As duas dependem da T1 
    t3.set_upstream(t4)          # A T3 depende da T4

pipeline()