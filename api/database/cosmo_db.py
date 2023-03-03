import os
import azure

from dotenv import load_dotenv
from azure.cosmos import CosmosClient, PartitionKey

load_dotenv()

DATABASE_NAME = "Assist-Tech-Challenge-DB"
USERS_CONTAINER_NAME = "users-container"
FORMS_CONTAINER_NAME = "forms-container"
SUBMITTED_FORMS_CONTAINER_NAME = "form-submits-container"

COSMOS_ENDPOINT = os.getenv('COSMOS_ENDPOINT')
COSMOS_KEY = os.getenv('COSMOS_KEY')

client = CosmosClient(url=COSMOS_ENDPOINT, credential=COSMOS_KEY)

# Connect to the db
database = client.create_database_if_not_exists(id=DATABASE_NAME)


# Create a new container for each "category" like users, forms, docs, etc
user_key = PartitionKey(path="/id")
users_container: azure.cosmos.container.ContainerProxy = database.create_container_if_not_exists(
    id=USERS_CONTAINER_NAME, partition_key=user_key, offer_throughput=400
)

form_key_path = PartitionKey(path="/id")
forms_container = database.create_container_if_not_exists(
    id=FORMS_CONTAINER_NAME, partition_key=form_key_path, offer_throughput=400
)

form_submits_key_path = PartitionKey(path="/id")
form_submits_container = database.create_container_if_not_exists(
    id=SUBMITTED_FORMS_CONTAINER_NAME, partition_key=form_key_path, offer_throughput=400
)




