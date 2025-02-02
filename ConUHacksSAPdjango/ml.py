import os
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
from sklearn.preprocessing import StandardScaler

# Step 1: Load Historical Data
wildfire_data = pd.read_csv('historical_wildfiredata.csv')  # Replace with your actual file path
environmental_data = pd.read_csv('historical_environmental_data.csv')  # Replace with your actual file path

# Convert timestamps to datetime
wildfire_data['timestamp'] = pd.to_datetime(wildfire_data['timestamp'])
environmental_data['timestamp'] = pd.to_datetime(environmental_data['timestamp'])

# Merge the data on timestamp and location (latitude, longitude)
merged_data = pd.merge(wildfire_data, environmental_data, on=['timestamp', 'latitude', 'longitude'])

# Feature Engineering: Extract temporal features and seasons
merged_data['hour'] = merged_data['timestamp'].dt.hour
merged_data['month'] = merged_data['timestamp'].dt.month
merged_data['weekday'] = merged_data['timestamp'].dt.weekday
merged_data['season'] = merged_data['month'].apply(lambda x: 'Winter' if x in [12, 1, 2] else 
                                                  ('Spring' if x in [3, 4, 5] else 
                                                   ('Summer' if x in [6, 7, 8] else 'Fall')))

# Create target variable: 1 if severity is not 'low', 0 if severity is 'low'
merged_data['target'] = merged_data['severity'].apply(lambda x: 1 if x != 'low' else 0)

# Step 2: Define Features and Target
features = ['temperature', 'humidity', 'wind_speed', 'precipitation', 'vegetation_index', 
            'human_activity_index', 'hour', 'month', 'weekday']
X = merged_data[features]
y = merged_data['target']

# Step 3: Scale the Features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 4: Split Data into Training and Testing Sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Step 5: Hyperparameter Tuning using GridSearchCV
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(estimator=RandomForestClassifier(random_state=42), param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
grid_search.fit(X_train, y_train)

# Get the best model
best_model = grid_search.best_estimator_

# Step 6: Evaluate the Model
y_pred = best_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')
print(classification_report(y_test, y_pred))

# Step 7: Visualize One of the Decision Trees (Optional)
plt.figure(figsize=(20, 10))
plot_tree(best_model.estimators_[0], feature_names=features, filled=True)
plt.savefig('wildfire_model_tree.png', dpi=300)
plt.show()

# Step 8: Save the Best Model to Disk (PKL File)
joblib.dump(best_model, 'best_wildfire_model.pkl')

# Step 9: Predict Future Fire Occurrences

# Load future environmental data (replace with your actual future data file)
future_data = pd.read_csv('future_environmental_data.csv')

# Preprocess future data (same steps as historical data)
future_data['timestamp'] = pd.to_datetime(future_data['timestamp'])  # Ensure the timestamp is in datetime format

# Feature Engineering: Extract temporal features for future data
future_data['hour'] = future_data['timestamp'].dt.hour
future_data['month'] = future_data['timestamp'].dt.month
future_data['weekday'] = future_data['timestamp'].dt.weekday
future_data['season'] = future_data['month'].apply(lambda x: 'Winter' if x in [12, 1, 2] else 
                                                  ('Spring' if x in [3, 4, 5] else 
                                                   ('Summer' if x in [6, 7, 8] else 'Fall')))

# Print the first few rows to verify
print(future_data.head())

# Select only the relevant features for prediction
future_X = future_data[features]

# Scale the future data using the same scaler
future_X_scaled = scaler.transform(future_X)

# Make predictions for future fire occurrences (using probabilities)
probabilities = best_model.predict_proba(future_X_scaled)

# Adjust the threshold for predicting a fire (e.g., 0.7 means the model needs to be more confident)
threshold = 0.7

# Get the predicted classes based on the threshold
predicted_fire = (probabilities[:, 1] >= threshold).astype(int)

# Add predictions to the future data
future_data['predicted_fire'] = predicted_fire

# Filter the rows where fire is predicted (predicted_fire == 1)
predicted_fire_data = future_data[future_data['predicted_fire'] == 1]

# Step 10: Save the Future Predictions with Location (Only Where Fire is Predicted) to a CSV File
# Only include rows where predicted_fire is 1
predicted_fire_data[['timestamp', 'latitude', 'longitude', 'predicted_fire']].to_csv('predicted_wildfire_occurrences_with_location.csv', index=False)

# Optionally display the future predictions along with location
print(predicted_fire_data[['timestamp', 'latitude', 'longitude', 'predicted_fire']])
