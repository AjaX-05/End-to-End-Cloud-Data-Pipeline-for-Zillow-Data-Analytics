import json
import boto3
import pandas as pd

s3_client = boto3.client("s3")

def lambda_handler(event, context):
    source_bucket = event["Records"][0]["s3"]["bucket"]["name"]
    object_key = event["Records"][0]["s3"]["object"]["key"]
    
    # print(source_bucket)
    # print(object_key)
    
    target_bucket = "transformed-of-silverzone-json-csv-bucket-s3-gold"
    target_file_name = object_key[:-5]
    
    waiter = s3_client.get_waiter("object_exists")
    waiter.wait(Bucket=source_bucket,Key=object_key)
    
    response = s3_client.get_object(Bucket=source_bucket,Key=object_key)
    # print(response)
    data = response["Body"]
    # print(data)
    data = response["Body"].read().decode("utf-8")
    # print(data)
    data = json.loads(data)
    # print(data)
    
    
    f = []
    for x in data['results']:
        f.append(x)
    df = pd.DataFrame(f)
    
    # Selecting specfic cols
    selected_cols = ['bathrooms', 'bedrooms' , 'city' ,'homeStatus', 'homeType', 'livingArea' , 'price' , 'rentZestimate','zipcode']
    
    df = df[selected_cols]
    print(df)
    
    # Convert DataFrame to CSV Format
    csv_data = df.to_csv(index=False)
    
    # Upload CSV to S3 Golden Layer
    bucket_name = target_bucket
    object_key = f"{target_file_name}.csv"
    s3_client.put_object(Bucket=bucket_name,Key=object_key,Body=csv_data)
    
    return{
        'statusCode':200,
        'body': json.dumps("CSV conversion and s3 upload completed sucessfully!")
    }