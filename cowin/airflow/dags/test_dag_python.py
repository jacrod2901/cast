from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago


def start():
    return f'sending email at:  {datetime.now()} '

def end():
    return f'Sent Notification Successfully'


default_args = {
    "owner": "ORCA",
    "depends_on_past": False,
    "start_date": datetime(2020, 5, 3),
    "email": ["jacrod2901@gmail.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id = "send_email",
    description="Send Email DAG",
    schedule_interval="*/10 * * * *",
    default_args=default_args,
    catchup=False,
) as dag:

    
    t1 = PythonOperator(
        task_id='START',
        provide_context=True,
        python_callable= start,
    )

    t2 = BashOperator(
        task_id='SendEmail',
        bash_command= 'python3 /home/jacrod2901/geese/cowin/Bootstrapper.py --coreconfig /home/jacrod2901/geese/cowin/resources/core-config.yaml --componentconfig /home/jacrod2901/geese/cowin/resources/sendnotification.yaml',
    )

    t3 = PythonOperator(
        task_id='END',
        provide_context=True,
        python_callable= end,
    )

t1 >> t2 >> t3

    
