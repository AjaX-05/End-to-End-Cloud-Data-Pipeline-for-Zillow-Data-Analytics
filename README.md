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

1. **Spin Up an EC2 Instance:**
   - Launch an EC2 t2.medium instance and configure it as needed.

2. **Connect to Your EC2 Instance:**
   - SSH into your EC2 instance to start the setup process.

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
   - The Lambda functions are responsible for data transformation and processing. The API key used for accessing the Rapid API is handled securely by storing it in a separate `.json` file. This file is not included in the code repository for security reasons.
   - You can deploy the Lambda functions using the following scripts:
     - [Copy From S3 Bronze to S3 Silver Lambda Function](https://github.com/AjaX-05/End-to-End-Cloud-Data-Pipeline-for-Zillow-Data-Analytics/blob/main/lambda_function1.py)
     - [Transform and Load to S3 Golden Lambda Function](https://github.com/AjaX-05/End-to-End-Cloud-Data-Pipeline-for-Zillow-Data-Analytics/blob/main/lambda_function2.py)

9. **Set Up Redshift:**
   - Provision a Redshift cluster, log in using your credentials, and create the required table for data loading. The table schema is as follows:
   
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

   - Apache Airflow will automate the process of bringing data from S3 to Redshift using the `S3ToRedshiftOperator`. AWS Access Key and password, along with Redshift endpoints, are configured in the Airflow UI itself.

## Airflow DAG
The Airflow DAG automates the entire pipeline workflow, including:

1. **Extracting Data**: Using the `PythonOperator` to call the `extract_zillow_data` function, which retrieves data from the Zillow API and stores it as a JSON file.
2. **Loading to S3**: Using the `BashOperator` to move the JSON file to an S3 bucket.
3. **Checking File Availability**: Using the `S3KeySensor` to ensure the file is available in S3.
4. **Transferring to Redshift**: Using the `S3ToRedshiftOperator` to load the CSV file from S3 into Redshift.

The code for this DAG is available [here](https://github.com/AjaX-05/End-to-End-Cloud-Data-Pipeline-for-Zillow-Data-Analytics/blob/main/zillowanalytics.py).

## Lambda Functions

### Copy From S3 Bronze to S3 Silver
The Lambda function `copyFromS3BronzeToS3Silver` copies data from the S3 Bronze bucket (Landing Zone) to the S3 Silver bucket (Intermediate Zone). Here’s how it works:
1. **Trigger**: The function is triggered by S3 events, which provide the source bucket and object key.
2. **Waiter**: It uses an S3 waiter to ensure the object exists in the source bucket before proceeding.
3. **Copy**: It copies the object to the target bucket (S3 Silver).
4. **Response**: The function returns a success message upon completion.

The code for this function is available [here](https://github.com/AjaX-05/End-to-End-Cloud-Data-Pipeline-for-Zillow-Data-Analytics/blob/main/lambda_function1.py).

### Transform and Load to S3 Golden
The Lambda function `transformation-convert-to-csv-s3golden-lambdafunction` performs data transformation and loads the processed data into the S3 Golden bucket. Here’s how it works:
1. **Trigger**: This function is triggered by S3 events from the S3 Silver bucket (Intermediate Zone).
2. **Waiter**: It waits for the object to be available in the source bucket before proceeding.
3. **Download and Transform**: It retrieves the JSON object, converts it to a Pandas DataFrame, selects specific columns, and converts the DataFrame to CSV format.
4. **Upload**: The CSV data is uploaded to the S3 Golden bucket.
5. **Response**: The function returns a success message upon completion.

The code for this function is available [here](https://github.com/AjaX-05/End-to-End-Cloud-Data-Pipeline-for-Zillow-Data-Analytics/blob/main/lambda_function2.py).

## QuickSight Visualization
![image](https://github.com/user-attachments/assets/2f3fb1b8-fbea-40e1-bbd5-6ec9359c9144)

For visualization, use AWS QuickSight to connect to the Redshift cluster and create dashboards and reports based on the data.

## Conclusion
This pipeline demonstrates a robust end-to-end solution for processing and analyzing Zillow data using various AWS services. By following the provided instructions, you can set up and deploy the pipeline to gain valuable insights from real estate data.

## Lessons Learned
Throughout this project, I have gained valuable insights and experience in the following areas:
- **End-to-End Data Pipelines**: Understanding the integration of multiple AWS services to create a seamless data pipeline.
- **AWS Lambda**: Implementing serverless functions for data processing and transformation.
- **Apache Airflow**: Automating and orchestrating complex workflows with DAGs.
- **Data Transformation**: Handling and converting data formats between JSON and CSV using Python.
- **Data Warehousing**: Configuring and managing data in Amazon Redshift.
- **Data Visualization**: Creating impactful visualizations and reports using AWS QuickSight.
- **Security Best Practices**: Managing sensitive information, such as API keys and credentials, securely within the project.

## Mistakes and Resolutions
1. **Region Configuration Issues**: Initially, I created S3 buckets and Lambda functions in different regions, which caused issues with data processing. Recreating these resources in the same region resolved the problem.
2. **EC2 Instance Region Mismatch**: I initially created the EC2 instance in a different region from S3, Lambda, and Redshift, leading to failures with the `S3ToRedshiftOperator`. After taking a snapshot of the EC2 instance and moving it to the same region as the other resources, the issue was resolved.
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

1. **Spin Up an EC2 Instance:**
   - Launch an EC2 t2.medium instance and configure it as needed.

2. **Connect to Your EC2 Instance:**
   - SSH into your EC2 instance to start the setup process.

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
   - The Lambda functions are responsible for data transformation and processing. The API key used for accessing the Rapid API is handled securely by storing it in a separate `.json` file. This file is not included in the code repository for security reasons.
   - You can deploy the Lambda functions using the following scripts:
     - [Copy From S3 Bronze to S3 Silver Lambda Function](https://github.com/AjaX-05/End-to-End-Cloud-Data-Pipeline-for-Zillow-Data-Analytics/blob/main/lambda_function1.py)
     - [Transform and Load to S3 Golden Lambda Function](https://github.com/AjaX-05/End-to-End-Cloud-Data-Pipeline-for-Zillow-Data-Analytics/blob/main/lambda_function2.py)

9. **Set Up Redshift:**
   - Provision a Redshift cluster, log in using your credentials, and create the required table for data loading. The table schema is as follows:
   
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

   - Apache Airflow will automate the process of bringing data from S3 to Redshift using the `S3ToRedshiftOperator`. AWS Access Key and password, along with Redshift endpoints, are configured in the Airflow UI itself.

## Airflow DAG
The Airflow DAG automates the entire pipeline workflow, including:

1. **Extracting Data**: Using the `PythonOperator` to call the `extract_zillow_data` function, which retrieves data from the Zillow API and stores it as a JSON file.
2. **Loading to S3**: Using the `BashOperator` to move the JSON file to an S3 bucket.
3. **Checking File Availability**: Using the `S3KeySensor` to ensure the file is available in S3.
4. **Transferring to Redshift**: Using the `S3ToRedshiftOperator` to load the CSV file from S3 into Redshift.

The code for this DAG is available [here](https://github.com/AjaX-05/End-to-End-Cloud-Data-Pipeline-for-Zillow-Data-Analytics/blob/main/zillowanalytics.py).

## Lambda Functions

### Copy From S3 Bronze to S3 Silver
The Lambda function `copyFromS3BronzeToS3Silver` copies data from the S3 Bronze bucket (Landing Zone) to the S3 Silver bucket (Intermediate Zone). Here’s how it works:
1. **Trigger**: The function is triggered by S3 events, which provide the source bucket and object key.
2. **Waiter**: It uses an S3 waiter to ensure the object exists in the source bucket before proceeding.
3. **Copy**: It copies the object to the target bucket (S3 Silver).
4. **Response**: The function returns a success message upon completion.

The code for this function is available [here](https://github.com/AjaX-05/End-to-End-Cloud-Data-Pipeline-for-Zillow-Data-Analytics/blob/main/lambda_function1.py).

### Transform and Load to S3 Golden
The Lambda function `transformation-convert-to-csv-s3golden-lambdafunction` performs data transformation and loads the processed data into the S3 Golden bucket. Here’s how it works:
1. **Trigger**: This function is triggered by S3 events from the S3 Silver bucket (Intermediate Zone).
2. **Waiter**: It waits for the object to be available in the source bucket before proceeding.
3. **Download and Transform**: It retrieves the JSON object, converts it to a Pandas DataFrame, selects specific columns, and converts the DataFrame to CSV format.
4. **Upload**: The CSV data is uploaded to the S3 Golden bucket.
5. **Response**: The function returns a success message upon completion.

The code for this function is available [here](https://github.com/AjaX-05/End-to-End-Cloud-Data-Pipeline-for-Zillow-Data-Analytics/blob/main/lambda_function2.py).

## QuickSight Visualization
![image](https://github.com/user-attachments/assets/2f3fb1b8-fbea-40e1-bbd5-6ec9359c9144)

For visualization, use AWS QuickSight to connect to the Redshift cluster and create dashboards and reports based on the data.

## Conclusion
This pipeline demonstrates a robust end-to-end solution for processing and analyzing Zillow data using various AWS services. By following the provided instructions, you can set up and deploy the pipeline to gain valuable insights from real estate data.

## Lessons Learned
Throughout this project, I have gained valuable insights and experience in the following areas:
- **End-to-End Data Pipelines**: Understanding the integration of multiple AWS services to create a seamless data pipeline.
- **AWS Lambda**: Implementing serverless functions for data processing and transformation.
- **Apache Airflow**: Automating and orchestrating complex workflows with DAGs.
- **Data Transformation**: Handling and converting data formats between JSON and CSV using Python.
- **Data Warehousing**: Configuring and managing data in Amazon Redshift.
- **Data Visualization**: Creating impactful visualizations and reports using AWS QuickSight.
- **Security Best Practices**: Managing sensitive information, such as API keys and credentials, securely within the project.

## Mistakes and Resolutions
1. **Region Configuration Issues**: Initially, I created S3 buckets and Lambda functions in different regions, which caused issues with data processing. Recreating these resources in the same region resolved the problem.
2. **EC2 Instance Region Mismatch**: I initially created the EC2 instance in a different region from S3, Lambda, and Redshift, leading to failures with the `S3ToRedshiftOperator`. After taking a snapshot of the EC2 instance and moving it to the same region as the other resources, the issue was resolved.
