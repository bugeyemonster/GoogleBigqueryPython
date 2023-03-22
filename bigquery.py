from google.cloud import bigquery

# Initialize the BigQuery client
client = bigquery.Client()

'''
use this command to make google creds availabel to the script as environment vars
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"

'''

# Define your query
query = '''
SELECT
  column1,
  column2
FROM
  your_project.your_dataset.your_table
'''

# Run the query and save the results to a temporary table
job_config = bigquery.QueryJobConfig(destination="your_project.your_dataset.temp_table", write_disposition="WRITE_TRUNCATE")
query_job = client.query(query, job_config=job_config)
query_job.result()  # Waits for the job to complete

# Export the temporary table to Google Cloud Storage
destination_uri = "gs://your_bucket_name/your_file_name.csv"
dataset_ref = client.dataset("your_dataset")
table_ref = dataset_ref.table("temp_table")
extract_job = client.extract_table(table_ref, destination_uri, location="US", job_config=bigquery.ExtractJobConfig(destination_format="CSV", field_delimiter=",", print_header=True))
extract_job.result()  # Waits for the job to complete

# Optionally, delete the temporary table after export
client.delete_table(table_ref)

print(f"Exported {table_ref.project}.{table_ref.dataset_id}.{table_ref.table_id} to {destination_uri}")