from azure.ai.ml import MLClient, command, Input
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()

ml_client = MLClient.from_config(credential=credential)

job = command(
    code="./",
    command="python azure_ml/train.py "
            "--orders_data ${{inputs.orders_data}} "
            "--customers_data ${{inputs.customers_data}}",

    inputs={
        "orders_data": Input(
            type="uri_file",
            path="azureml:orders-data-new:1"
        ),
        "customers_data": Input(
            type="uri_file",
            path="azureml:customers-data-new:1"
        ),
    },
    environment="azureml:crm360-final-env:1",
    compute="gnanasrihasa1"
)

print("Step 2: Job object created")

returned_job = ml_client.jobs.create_or_update(job)

print("Step 3: Job submitted")

print(returned_job.name)