from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
from transform import transform_data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 9, 7),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'transform_dag',
    default_args=default_args,
    description='transform KickStats data',
    schedule_interval=timedelta(days=1),
)

transform_etl = PythonOperator(
    task_id='transform_dataset',
    python_callable=transform_data,
    dag=dag,
)

transform_etl