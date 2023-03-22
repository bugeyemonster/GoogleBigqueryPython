from google.cloud import bigquery

# Initialize the BigQuery client
client = bigquery.Client()

# Get the list of datasets in the project
datasets = list(client.list_datasets())

# Iterate through the datasets
for dataset in datasets:
    dataset_ref = client.dataset(dataset.dataset_id)
    
    # Get the list of tables in the dataset
    tables = list(client.list_tables(dataset_ref))
    
    # Iterate through the tables
    for table in tables:
        table_ref = dataset_ref.table(table.table_id)
        table_obj = client.get_table(table_ref)
        
        # Create a SELECT * query for the table
        query = f'SELECT * FROM `{table_obj.project}.{table_obj.dataset_id}.{table_obj.table_id}`'
        
        # Execute the query and get the results
        query_job = client.query(query)
        results = query_job.result()
        
        # Process the results as needed (e.g., print, save to file, etc.)
        for row in results:
            print(row)
