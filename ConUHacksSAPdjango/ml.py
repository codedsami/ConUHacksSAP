import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

wildfire_data = pd.read_csv('historical_wildfiredata.csv')
environmental_data = pd.read_csv('historical_environmental_data.csv')

# # Query data from MongoDB for historical wildfire occurrences
# wildfire_data = HistoricalFireEvents.objects.all()

# # Query environmental data (can also filter based on timestamp or other conditions)
# environmental_data = HistoricalEnvironmentalData.objects.all()

# Convert timestamp to datetime for easier merging
wildfire_data['timestamp'] = pd.to_datetime(wildfire_data['timestamp'])
environmental_data['timestamp'] = pd.to_datetime(environmental_data['timestamp'])

# Merge the historical data on timestamp and location
merged_data = pd.merge(wildfire_data, environmental_data, on=['timestamp', 'latitude', 'longitude'])

merged_data['target'] = merged_data['severity'].apply(lambda x: 1 if x != 'low' else 0)
# Define features and target
features = ['temperature', 'humidity', 'wind_speed', 'precipitation', 'vegetation_index', 'human_activity_index']
# Target: fire occurrence (binary)
X = merged_data[features]
y = merged_data['target']
# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the RandomForest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
# draw model and display it
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

plt.figure(figsize=(20,10))
plot_tree(model.estimators_[0], feature_names=features, filled=True)
plt.savefig('wildfire_model_tree.png', dpi=300)
plt.show()
# save the model to disk in pk1 format
joblib.dump(model, 'wildfire_model.pkl')
