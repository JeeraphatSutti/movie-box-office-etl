from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "bundi",
    "retries": 1,
}

with DAG(
    dag_id="movies_pipeline",
    description="Bronze -> Silver -> Gold movies ETL",
    start_date=datetime(2024, 1, 1),
    schedule=None,          
    catchup=False,
    default_args=default_args,
    tags=["movies", "etl"],
) as dag:

    bronze = BashOperator(
        task_id="bronze",
        bash_command="python /opt/airflow/src/bronze_ingest.py",
    )

    silver = BashOperator(
        task_id="silver",
        bash_command="python /opt/airflow/src/silver_transform.py",
    )

    gold = BashOperator(
        task_id="gold",
        bash_command="python /opt/airflow/src/gold_aggregate.py",
    )


    bronze >> silver >> gold
