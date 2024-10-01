"""
data_ingestion_dag.py

Ce module définit un Directed Acyclic Graph (DAG) pour l'ingestion de données et le
modélisation avec Apache Airflow.

Dépendances:
- Apache Airflow: Ce module utilise les classes DAG, PythonOperator et BashOperator de 
  la bibliothèque Airflow pour orchestrer les tâches.
- La fonction `execute_data_ingestion` est importée depuis le module `data_ingestion`
  et est utilisée pour ingérer des données.

Description du DAG:
- Le DAG est nommé "data_ingestion_dag" et est configuré pour s'exécuter quotidiennement 
  à partir de la date de début spécifiée (29 septembre 2024).
- Les paramètres par défaut du DAG incluent le propriétaire défini sur "airflow".
  
Tâches définies:
1. `ingest_data_task`: Utilise le PythonOperator pour exécuter la fonction 
   `execute_data_ingestion`, qui est responsable de l'ingestion des données.
   
2. `modeling_data_task`: Utilise le BashOperator pour exécuter une commande bash 
   qui change le répertoire vers le projet DBT et exécute `dbt run`, utilisant 
   les profils stockés dans le répertoire de modélisation d'Airflow.

Les tâches sont dépendantes, où `ingest_data_task` doit être terminée avant que 
`modeling_data_task` puisse commencer.
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

# Import de la fonction de ton script
from data_ingestion import execute_data_ingestion

default_args = {"owner": "airflow", "start_date": datetime(2024, 9, 29)}

with DAG("data_ingestion_dag", default_args=default_args, schedule="@daily") as dag:

    ingest_data_task = PythonOperator(
        task_id="ingest_data", python_callable=execute_data_ingestion
    )

    modeling_data_task = BashOperator(
        task_id="dbt_run",
        bash_command="cd ${AIRFLOW_HOME}/modeling/dbt_project && dbt run --profiles-dir ${AIRFLOW_HOME}/modeling/",
    )

ingest_data_task >> modeling_data_task
