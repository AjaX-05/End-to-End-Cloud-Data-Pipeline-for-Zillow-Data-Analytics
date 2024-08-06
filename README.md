# End-to-End Cloud Data Pipeline for Zillow Data Analytics

## Table of Contents
1. [Introduction](#introduction)
2. [Architecture](#architecture)
3. [Technologies Used](#technologies-used)
4. [Setup and Configuration](#setup-and-configuration)
5. [Airflow DAG](#airflow-dag)
6. [Lambda Functions](#lambda-functions)
    - [Copy From S3 Bronze to S3 Silver](#copy-from-s3-bronze-to-s3-silver)
    - [Transform and Load to S3 Golden](#transform-and-load-to-s3-golden)
7. [Redshift Configuration](#redshift-configuration)
8. [QuickSight Visualization](#quicksight-visualization)
9. [Conclusion](#conclusion)
10. [Lessons Learned](#lessons-learned)
11. [Mistakes and Resolutions](#mistakes-and-resolutions)

## Introduction
This project demonstrates the creation of an end-to-end cloud data pipeline using AWS services to extract, process, and visualize Zillow data. The pipeline integrates multiple services including AWS Lambda, S3, Redshift, and QuickSight, orchestrated using Apache Airflow running on an EC2 instance.

## Architecture
![Architecture Diagram](https://github.com/user-attachments/assets/0e607b15-400a-4850-bf02-9769df341128)

## Technologies Used
- **AWS S3**: For data storage across different stages.
- **AWS Lambda**: For serverless data processing and transformation.
- **AWS Redshift**: For data warehousing.
- **AWS QuickSight**: For data visualization.
- **Apache Airflow**: For orchestrating the data pipeline.
- **Amazon EC2**: For running Apache Airflow and executing Python code.
- **Rapid API**: For extracting data from Zillow.
- **Pandas**: For data manipulation and transformation.
- **Requests**: For making API calls.

## Setup and Configuration
1. **Spin Up an EC2 Instance:**
   - Launch an EC2 t2.medium instance and configure it according to your requirements.

2. **Connect to Your EC2 Instance:**
   - SSH into the EC2 instance to start the setup process.

3. **Update Package Lists and Install Dependencies:**

    ```bash
    sudo apt update
    sudo apt install python3-pip
    sudo apt install python3.10-venv
    ```

4. **Create and Activate a Virtual Environment:**

    ```bash
    python3 -m venv myenv
    source myenv/bin/activate
    ```

5. **Install AWS CLI and Apache Airflow:**

    ```bash
    pip install --upgrade awscli
    pip install apache-airflow
    airflow standalone
    ```

6. **Install Airflow Providers for Amazon:**

    ```bash
    pip install apache-airflow-providers-amazon
    ```

7. **Set Up Apache Airflow:**
   - The Airflow DAG script orchestrates the entire pipeline workflow:
     - [Airflow DAG Script](https://github.com/AjaX-05/End-to-End-Cloud-Data-Pipeline-for-Zillow-Data-Analytics/blob/main/zillowanalytics.py)

8. **Deploy Lambda Functions:**
   - Deploy the Lambda functions responsible for data processing:
     - [Copy From S3 Bronze to S3 Silver Lambda Function](https://github.com/AjaX-05/End-to-End-Cloud-Data-Pipeline-for-Zillow-Data-Analytics/blob/main/lambda_function1.py)
     - [Transform and Load to S3 Golden Lambda Function](https://github.com/AjaX-05/End-to-End-Cloud-Data-Pipeline-for-Zillow-Data-Analytics/blob/main/lambda_function2.py)

9. **Set Up Redshift:**
   - Provision a Redshift cluster and configure it for data warehousing. Create the required table using the following SQL script:
   
    ```sql
    CREATE TABLE IF NOT EXISTS zillowdata(
        bathrooms NUMERIC,
        bedrooms NUMERIC,
        city VARCHAR(255),
        homeStatus VARCHAR(255),
        homeType VARCHAR(255),
        livingArea NUMERIC,
        price NUMERIC,
        rentZestimate NUMERIC,
        zipcode INT
    );
    ```

   - Apache Airflow will automate the transfer of data from S3 to Redshift using the `S3ToRedshiftOperator`. AWS Access Key and secret, as well as Redshift endpoints, are configured directly in the Airflow UI for secure management.

## Airflow DAG
The Airflow DAG automates the pipeline workflow:

1. **Data Extraction**: Uses `PythonOperator` to call the `extract_zillow_data` function, which retrieves data from the Zillow API and stores it as a JSON file.
2. **Data Upload**: Uses `BashOperator` to move the JSON file to an S3 bucket.
3. **File Availability Check**: Uses `S3KeySensor` to ensure the file is available in S3.
4. **Data Transfer**: Uses `S3ToRedshiftOperator` to load the CSV file from S3 into Redshift.

The DAG script is available [here](https://github.com/AjaX-05/End-to-End-Cloud-Data-Pipeline-for-Zillow-Data-Analytics/blob/main/zillowanalytics.py).

## Lambda Functions

### Copy From S3 Bronze to S3 Silver
This Lambda function copies data from the S3 Bronze bucket (Landing Zone) to the S3 Silver bucket (Intermediate Zone). It:
1. **Trigger**: Activated by S3 events providing the source bucket and object key.
2. **Waiter**: Waits for the object to exist in the source bucket.
3. **Copy**: Copies the object to the target bucket (S3 Silver).
4. **Response**: Returns a success message.

The code for this function is available [here](https://github.com/AjaX-05/End-to-End-Cloud-Data-Pipeline-for-Zillow-Data-Analytics/blob/main/lambda_function1.py).

### Transform and Load to S3 Golden
This Lambda function performs data transformation and uploads the processed data to the S3 Golden bucket. It:
1. **Trigger**: Activated by S3 events from the S3 Silver bucket (Intermediate Zone).
2. **Waiter**: Waits for the object to be available in the source bucket.
3. **Download and Transform**: Retrieves the JSON object, converts it to a DataFrame, selects columns, and converts it to CSV format.
4. **Upload**: Uploads the CSV data to the S3 Golden bucket.
5. **Response**: Returns a success message.

The code for this function is available [here](https://github.com/AjaX-05/End-to-End-Cloud-Data-Pipeline-for-Zillow-Data-Analytics/blob/main/lambda_function2.py).

## QuickSight Visualization
![QuickSight Visualization](https://github.com/user-attachments/assets/2f3fb1b8-fbea-40e1-bbd5-6ec9359c9144)

Create impactful visualizations and reports in AWS QuickSight using data from Redshift.

## Conclusion
This project showcases an end-to-end solution for processing and analyzing Zillow data using AWS services. By following the instructions, you can set up and deploy a comprehensive data pipeline for real estate analytics.

## Lessons Learned
Throughout this project, I have gained valuable insights and experience in the following areas:
- **End-to-End Data Pipelines**: Integrating multiple AWS services to create a seamless data pipeline.
- **AWS Lambda**: Implementing serverless functions for data processing and transformation.
- **Apache Airflow**: Automating and orchestrating complex workflows with DAGs.
- **Data Transformation**: Handling and converting data formats between JSON and CSV using Python.
- **Data Warehousing**: Configuring and managing data in Amazon Redshift.
- **Data Visualization**: Creating impactful visualizations and reports using AWS QuickSight.
- **Security Best Practices**: Managing sensitive information securely within the project.

## Mistakes and Resolutions
1. **Region Configuration Issues**: Initially, I created S3 buckets and Lambda functions in different regions, which caused issues with data processing. Recreating these resources in the same region resolved the problem.
2. **EC2 Instance Region Mismatch**: The EC2 instance was initially created in a different region from S3, Lambda, and Redshift, leading to failures with the `S3ToRedshiftOperator`. After taking a snapshot of the EC2 instance and moving it to the same region as the other resources, the issue was resolved.
