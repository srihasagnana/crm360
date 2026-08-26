from azure.ai.ml import MLClient
from azure.ai.ml.entities import (
    ManagedOnlineEndpoint,
    ManagedOnlineDeployment,
    CodeConfiguration,
)
from azure.identity import DefaultAzureCredential

# ----------------------------------
# Connect to Azure ML Workspace
# ----------------------------------

credential = DefaultAzureCredential()

ml_client = MLClient.from_config(credential=credential)

print("Connected to Azure ML")

# ----------------------------------
# Create Endpoint
# ----------------------------------

endpoint = ManagedOnlineEndpoint(
    name="crm360-endpoint-sdk",
    description="CRM360 Churn Prediction Endpoint",
    auth_mode="key",
)

print("Creating endpoint...")

ml_client.online_endpoints.begin_create_or_update(endpoint).result()

print("Endpoint created successfully")

# ----------------------------------
# Create Deployment
# ----------------------------------

deployment = ManagedOnlineDeployment(
    name="blue",
    endpoint_name="crm360-endpoint-sdk",

    model="azureml:crm360-churn-rf:1",

    environment="azureml:crm360-final-env-latest-1:1",

    code_configuration=CodeConfiguration(
        code="./",
        scoring_script="score.py",
    ),

    instance_type="Standard_DS2_v2",
    instance_count=1,
)

print("Creating deployment...")

ml_client.online_deployments.begin_create_or_update(deployment).result()

print("Deployment created successfully")

# ----------------------------------
# Route 100% traffic
# ----------------------------------

endpoint.traffic = {
    "blue": 100
}

ml_client.online_endpoints.begin_create_or_update(endpoint).result()

print("Deployment Complete!")