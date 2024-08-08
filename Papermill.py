from airflow import DAG
from airflow.providers.papermill.operators.papermill import PapermillOperator
from airflow.operators.email_operator import EmailOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from airflow.exceptions import AirflowException

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': True,  # To send emails on retries as well
    'email': ['your_email@example.com'],  # Replace with your email
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'papermill_operator_dag',
    default_args=default_args,
    description='Execute a Jupyter notebook with Papermill and send an email on failure',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    catchup=False,
)

# Task to run the notebook with PapermillOperator
run_notebook_task = PapermillOperator(
    task_id='run_notebook',
    input_nb='path/to/your/example_notebook.ipynb',  # Input notebook path
    output_nb='path/to/output_notebook_{{ execution_date }}.ipynb',  # Output notebook path with timestamp
    parameters={'param1': 'value1', 'param2': 100},
    dag=dag,
)

# Function to send an email if the task fails
def send_failure_email(context):
    # Create the email operator inside the failure callback
    email_task = EmailOperator(
        task_id='send_failure_email',
        to='your_email@example.com',  # Replace with your email
        subject=f"Airflow Task Failed: {context['task_instance'].task_id}",
        html_content=f"""
        <h3>Task Failed</h3>
        <p><strong>Task ID:</strong> {context['task_instance'].task_id}</p>
        <p><strong>DAG ID:</strong> {context['task_instance'].dag_id}</p>
        <p><strong>Execution Date:</strong> {context['execution_date']}</p>
        <p><strong>Log URL:</strong> <a href="{context['task_instance'].log_url}">View Log</a></p>
        """,
        dag=dag,
    )
    # Execute the email task manually
    email_task.execute(context)

# Attach the email failure callback to the task
run_notebook_task.on_failure_callback = send_failure_email

# Define task dependencies
run_notebook_task
