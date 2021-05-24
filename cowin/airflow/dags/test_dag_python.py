from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from test.email_test import send_email


def hello_world():
    return f'sending email at:  {datetime.now()} '

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
    dag_id = "python_dag",
    description="Simple tutorial DAG",
    schedule_interval="*/2 * * * *",
    default_args=default_args,
    catchup=False,
) as dag:

    
    t1 = PythonOperator(
        task_id='helloworld',
        provide_context=True,
        python_callable=hello_world,
    )

    t2 = PythonOperator(
        task_id='SendEmail',
        provide_context=True,
        python_callable=send_email(),
    )

t1 >> t2

    
