import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

# Step 1: Load Historical Data
wildfire_data = pd.read_csv('historical_wildfiredata.csv')  # Replace with your actual file path
environmental_data = pd.read_csv('historical_environmental_data.csv')  # Replace with your actual file path

# Convert timestamps to datetime for easier merging
wildfire_data['timestamp'] = pd.to_datetime(wildfire_data['timestamp'])
environmental_data['timestamp'] = pd.to_datetime(environmental_data['timestamp'])

# Merge the wildfire data with environmental data based on timestamp and location
merged_data = pd.merge(wildfire_data, environmental_data, on=['timestamp', 'latitude', 'longitude'])

# Create target variable: 1 if severity is not 'low', 0 if severity is 'low'
merged_data['target'] = merged_data['severity'].apply(lambda x: 1 if x != 'low' else 0)

# Step 2: Define Features and Target
features = ['temperature', 'humidity', 'wind_speed', 'precipitation', 'vegetation_index', 'human_activity_index']
X = merged_data[features]
y = merged_data['target']

# Step 3: Split the Data into Training and Test Sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Create and Train the Random Forest Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 5: Evaluate the Model
y_pred = model.predict(X_test)

# Print accuracy and classification report
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')
print(classification_report(y_test, y_pred))

# Step 6: Visualize One of the Decision Trees
plt.figure(figsize=(20, 10))
plot_tree(model.estimators_[0], feature_names=features, filled=True)
plt.savefig('wildfire_model_tree.png', dpi=300)
plt.show()

# Step 7: Save the Model to Disk (PKL File)
joblib.dump(model, 'wildfire_model.pkl')

# Step 8: Predict Future Fire Occurrences

# Load future environmental data
future_data = pd.read_csv('future_environmental_data.csv')  # Replace with your actual future data file

# Preprocess future data (same steps as historical data)
future_data['timestamp'] = pd.to_datetime(future_data['timestamp'])
future_data['month'] = future_data['timestamp'].dt.month
future_data['day'] = future_data['timestamp'].dt.day
future_data['weekday'] = future_data['timestamp'].dt.weekday

# Print the first few rows to verify the future data
print(future_data.head())

# Select only the relevant features for prediction
future_X = future_data[features]

# Make predictions for future fire occurrences
future_predictions = model.predict(future_X)

# Add predictions to the future data
future_data['predicted_fire'] = future_predictions

# Filter the rows where fire is predicted (predicted_fire == 1)
predicted_fire_data = future_data[future_data['predicted_fire'] == 1]

# Step 9: Save the Future Predictions with Location (Only Where Fire is Predicted) to a CSV File
# Only include rows where predicted_fire is 1
predicted_fire_data[['timestamp', 'latitude', 'longitude', 'predicted_fire']].to_csv('predicted_wildfire_occurrences_with_location.csv', index=False)

# Optionally display the future predictions along with location
print(predicted_fire_data[['timestamp', 'latitude', 'longitude', 'predicted_fire']])
