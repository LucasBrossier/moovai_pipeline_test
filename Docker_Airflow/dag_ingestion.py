from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

# Import de la fonction de ton script
from data_ingestion import execute_data_ingestion

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1)
}

with DAG("data_ingestion_dag",
         default_args=default_args,
         schedule="@daily") as dag:

    ingest_data_task = PythonOperator(
        task_id="ingest_data",
        python_callable=execute_data_ingestion
    )

    modeling_data_task = BashOperator(
        task_id="dbt_run",
        bash_command="cd ${AIRFLOW_HOME}/modeling/dbt_project && dbt run --profiles-dir ${AIRFLOW_HOME}/modeling/"
    )

ingest_data_task >> modeling_data_task