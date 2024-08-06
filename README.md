# End-to-End Cloud Data Pipeline for Zillow Data Analytics

## Table of Contents
1. [Introduction](#introduction)
2. [Architecture](#architecture)
3. [Technologies Used](#technologies-used)
4. [Setup and Configuration](#setup-and-configuration)
5. [Airflow DAG](#airflow-dag)
6. [Lambda Functions](#lambda-functions)
    - [Copy From S3 Bronze to S3 Silver]
    - [Transform and Load to S3 Golden]
7. [Deploy Lambda Functions](#deploy-lambda-functions)
8. [Redshift Configuration](#redshift-configuration)
9. [QuickSight Visualization](#quicksight-visualization)
10. [Conclusion](#conclusion)
11. [Screenshots](#screenshots)

## Introduction
This project demonstrates an end-to-end cloud data pipeline built using AWS services to extract data from Zillow using the Rapid API, process it through various stages, and visualize it using QuickSight. The pipeline is orchestrated using Apache Airflow running on an EC2 instance.

## Architecture
![image](https://github.com/user-attachments/assets/0e607b15-400a-4850-bf02-9769df341128)

## Technologies Used
- **AWS S3**: For data storage across different stages.
- **AWS Lambda**: For data transformation and processing.
- **AWS Redshift**: For data warehousing.
- **AWS QuickSight**: For data visualization.
- **Apache Airflow**: For orchestrating the pipeline.
- **Amazon EC2**: For running Apache Airflow, making Rapid API calls, and executing Python code with Pandas and Requests.
- **Rapid API**: For extracting data from Zillow.
- **Pandas**: For data manipulation and transformation.
- **Requests**: For making API calls.

## Setup and Configuration
Follow these steps to set up and configure the pipeline:

1. **Update Package Lists and Install Dependencies:**

    ```bash
    sudo apt update
    sudo apt install python3-pip
    sudo apt install python3.10-venv
    ```

2. **Create and Activate a Virtual Environment:**

    ```bash
    python3 -m venv myenv
    source myenv/bin/activate
    ```

3. **Install AWS CLI and Apache Airflow:**

    ```bash
    pip install --upgrade awscli
    sudo pip install apache-airflow
    airflow standalone
    ```

4. **Install Airflow Providers for Amazon:**

    ```bash
    pip install apache-airflow-providers-amazon
    ```

5. **Spin Up an EC2 Instance:**
   - Launch an EC2 t2.medium instance and configure it as needed.

6. **Set Up Apache Airflow:**
   - The Airflow DAG script orchestrates the entire pipeline workflow:
     - [Airflow DAG Script](https://github.com/AjaX-05/End-to-End-Cloud-Data-Pipeline-for-Zillow-Data-Analytics/blob/main/zillowanalytics.py)

7. **Deploy Lambda Functions:**
   - The Lambda functions are responsible for data transformation and processing. You can deploy them using the following scripts:
     - [Copy From S3 Bronze to S3 Silver Lambda Function](https://github.com/AjaX-05/End-to-End-Cloud-Data-Pipeline-for-Zillow-Data-Analytics/blob/main/lambda_function1.py)
     - [Transform and Load to S3 Golden Lambda Function](https://github.com/AjaX-05/End-to-End-Cloud-Data-Pipeline-for-Zillow-Data-Analytics/blob/main/lambda_function2.py)

8. **Set Up Redshift:**
   - I provisioned a Redshift cluster and accessed it using the administrator credentials. Following this, I created a table in Redshift to facilitate the data transfer process. The table is designed to receive data from the Gold layer, as managed by the S3Redshift operator in Apache Airflow.
   
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
