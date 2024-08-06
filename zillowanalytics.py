from airflow import DAG
from datetime import datetime, timedelta
import json
import requests
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor 
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator

with open('/home/ubuntu/airflow/config_api.json') as config_file:
    api_host_key = json.load(config_file)

now = datetime.now()
dt_now_string = now.strftime("%d%m%Y%H%M%S")

# Define the s3 bucket name
s3_bucket = 'transformed-of-silverzone-json-csv-bucket-s3-gold'

def extract_zillow_data(**kwargs):
    url = kwargs['url']
    headers = kwargs['headers']
    querystring = kwargs['querystring']
    dt_string = kwargs['date_string']
    # return headers
    response = requests.get(url, headers=headers , params=querystring)
    response_data = response.json()
    
    # Specify the output file path
    output_file_path = f"/home/ubuntu/response_data_{dt_string}.json"
    file_str = f"response_data_{dt_string}.csv"
    
    # Write the JSON response to a file
    with open(output_file_path, "w") as output_file:
        json.dump(response_data, output_file , indent=4)
        
    # returns json and csv files
    output_list = [output_file_path, file_str]
    return output_list

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024,7,28),
    'email': ['majaysakthishankar@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=15)
}

with DAG(
    'zillow_analytics_dag',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    catchup=False
) as dag:
    
    extract_zillow_data_var = PythonOperator(
        task_id="python_task_extract_zillow_data_var",
        python_callable=extract_zillow_data,
        # all the below operator KWargs will get unpacked by the callable function
        op_kwargs={"url" : "https://zillow56.p.rapidapi.com/search",
        "querystring" : {"location":"richardson, tx","output":"json","status":"forSale","sortSelection":"priorityscore","listing_type":"by_agent","doz":"any"},
        "headers": api_host_key,
        "date_string": dt_now_string}
    )
    
    load_to_s3 = BashOperator(
        task_id="tsk_load_to_s3",
        bash_command='/home/ubuntu/ZDA_env/bin/aws s3 mv {{ti.xcom_pull("python_task_extract_zillow_data_var")[0]}} s3://zillow-data-analytics-end-to-end-project-2024/'
    )
    
    is_file_in_s3_available = S3KeySensor(
        task_id='tsk_is_file_in_s3_available',
        bucket_key='{{ ti.xcom_pull("python_task_extract_zillow_data_var")[1] }}',
        bucket_name=s3_bucket,
        aws_conn_id='aws_s3_conn',
        wildcard_match=False,
        timeout=60,
        poke_interval=5 
    )
    
    transfer_s3_to_redshift = S3ToRedshiftOperator(
        task_id='tsk_transfer_s3_to_redshift',
        aws_conn_id='aws_s3_conn',
        redshift_conn_id='conn_id_redshift',
        s3_bucket=s3_bucket,
        s3_key='{{ ti.xcom_pull("python_task_extract_zillow_data_var")[1] }}',
        schema="public",
        table="zillowdata",
        copy_options=["csv IGNOREHEADER 1"]
    )
    
     
    extract_zillow_data_var >> load_to_s3 >> is_file_in_s3_available >> transfer_s3_to_redshift