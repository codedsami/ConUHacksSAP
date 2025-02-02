import pandas as pd
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os

# MongoDB Atlas Connection
# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI from environment variables
uri = os.getenv("MONGO_DATABASE_URL")
client = MongoClient(uri)

# Specify Database and Collection
db = client['mydatabase']
collection = db['backend_futureenvironmentaldata']

# Specify CSV file to import
csv_file = 'future_environmental_data.csv'
df = pd.read_csv(csv_file, sep=',')

# Convert DataFrame to dictionary format for MongoDB
data = df.to_dict(orient='records')

# Insert Data into MongoDB with auto-generated IDs
if data:
    for record in data:
        record['id'] = ObjectId()  # Add ObjectId to each record
    collection.insert_many(data)
    print(f"Successfully imported {len(data)} records to MongoDB!")
else:
    print("No data to import.")