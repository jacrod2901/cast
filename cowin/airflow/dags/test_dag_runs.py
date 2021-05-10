from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

def hello_world():
    return 'Printing hello world!'

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
    dag_id = "runs_dag",
    description="Simple tutorial DAG",
    schedule_interval="*/3 * * * *",
    default_args=default_args,
    catchup=False,
) as dag:

    
    t1 = PythonOperator(
        task_id='helloworld',
        provide_context=True,
        python_callable=hello_world,
    )

t1

    
