from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago



default_args = {
    "owner": "jacrod2901",
    "depends_on_past": False,
    "start_date": datetime(2020, 5, 3),
    "email": ["jacrod2901@gmail.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}


with DAG(
    dag_id = "bash_dag",
    description="Simple tutorial DAG",
    schedule_interval="*/2 * * * *",
    default_args=default_args,
) as dag:


     t1 = BashOperator(
        task_id='print_date',
        bash_command='date',
    )

t1