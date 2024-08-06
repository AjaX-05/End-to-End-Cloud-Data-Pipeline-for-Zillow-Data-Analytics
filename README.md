# End-to-End Cloud Data Pipeline for Zillow Data Analytics

## Table of Contents
1. [Introduction](#introduction)
2. [Architecture](#architecture)
3. [Technologies Used](#technologies-used)
4. [Setup and Configuration](#setup-and-configuration)
5. [Lambda Functions](#lambda-functions)
    - [Copy From S3 Bronze to S3 Silver](#copy-from-s3-bronze-to-s3-silver)
    - [Transform and Load to S3 Golden](#transform-and-load-to-s3-golden)
6. [Redshift Configuration](#redshift-configuration)
7. [Airflow DAG](#airflow-dag)
9. [Conclusion](#conclusion)
10. [Screenshots](#screenshots)

## Introduction
This project demonstrates an end-to-end cloud data pipeline built using AWS services to extract data from Zillow using the Rapid API, process it through various stages, and visualize it using QuickSight. The pipeline is orchestrated using Apache Airflow running on an EC2 instance.

## Architecture
![Architecture](https://github.com/AjaX-05/End-to-End-Cloud-Data-Pipeline-for-Zillow-Data-Analytics/blob/main/Project-Architecture.pdf)

## Technologies Used
- **AWS S3**: For data storage across different stages.
- **AWS Lambda**: For data transformation and processing.
- **AWS Redshift**: For data warehousing.
- **AWS QuickSight**: For data visualization.
- **Apache Airflow**: For orchestrating the pipeline.
- **Amazon EC2**: For hosting the Airflow instance.
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

5. **Deploy Lambda Functions:**
   - [Copy From S3 Bronze to S3 Silver Lambda Function](https://github.com/AjaX-05/End-to-End-Cloud-Data-Pipeline-for-Zillow-Data-Analytics/blob/main/lambda_function1.py)
   - [Transform and Load to S3 Golden Lambda Function](https://github.com/AjaX-05/End-to-End-Cloud-Data-Pipeline-for-Zillow-Data-Analytics/blob/main/lambda_function2.py)

6. **Set Up Redshift:**
   - [Redshift Cluster Setup and Schema](https://github.com/yourusername/yourrepo/blob/main/redshift_cluster_setup.py)
   - [Schema SQL](https://github.com/yourusername/yourrepo/blob/main/schema.sql)

7. **Set Up Apache Airflow:**
   - [Airflow DAG Script](https://github.com/AjaX-05/End-to-End-Cloud-Data-Pipeline-for-Zillow-Data-Analytics/blob/main/zillowanalytics.py)


## Conclusion
This project demonstrates a robust data pipeline for processing Zillow data using AWS services. The pipeline effectively extracts, transforms, and loads data, providing valuable insights through QuickSight visualizations.

## Result
- **QuickSight Visualization**: ![QuickSight Visualization](https://github.com/AjaX-05/End-to-End-Cloud-Data-Pipeline-for-Zillow-Data-Analytics/blob/main/Quicksight.png)
