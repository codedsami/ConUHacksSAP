import pandas as pd
from pymongo import MongoClient

# MongoDB Atlas Connection
uri = "mongodb+srv://<user>:<pass>@cluster0.9cgk7mn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)

# Specify Database and Collection
db = client['mydatabase']
collection = db['backend_currentfireevents']

# Correct CSV reading with comma as the separator
csv_file = 'wildfire.csv'
df = pd.read_csv(csv_file, sep=',')  # Change sep from '\t' to ','

# Add unique ID
df['_id'] = range(1, len(df) + 1)

# Convert DataFrame to dictionary format for MongoDB
data = df.to_dict(orient='records')

# Insert Data into MongoDB
if data:
    collection.insert_many(data)
    print(f"Successfully imported {len(data)} records to MongoDB!")
else:
    print("No data to import.")