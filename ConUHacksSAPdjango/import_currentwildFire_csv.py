import pandas as pd
from pymongo import MongoClient

# MongoDB Atlas Connection
# uri = something from environment variables
client = MongoClient(uri)

# Specify Database and Collection
db = client['mydatabase']
collection = db['backend_currentfireevents']

# Read CSV File
csv_file = 'wildfire.csv'  # Replace with your actual CSV file name
df = pd.read_csv(csv_file, sep='\t')  # Assuming tab-separated values

df['_id'] = range(1, len(df) + 1)
# Convert DataFrame to Dictionary Format for MongoDB
data = df.to_dict(orient='records')

# Insert Data into MongoDB
if data:
    collection.insert_many(data)
    print(f"Successfully imported {len(data)} records to MongoDB!")
else:
    print("No data to import.")