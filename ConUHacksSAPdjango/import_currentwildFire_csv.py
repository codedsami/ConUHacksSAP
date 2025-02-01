import os
import django
from django.utils import timezone
import pandas as pd
from datetime import datetime
from backend.models import CurrentFireEvents


# Set the Django settings module to the correct settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ConUHacksSAPdjango.settings')
print(f"DJANGO_SETTINGS_MODULE is set to: {os.getenv('DJANGO_SETTINGS_MODULE')}")



# Initialize Django
try:
    django.setup()
except Exception as e:
    print(f"Error initializing Django: {e}")
    raise

def parse_timestamp(timestamp_str):
    # Parse the timestamp with 24-hour format (no AM/PM)
    dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M")
    
    # Convert naive datetime to aware datetime using UTC (or your specific timezone)
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt, timezone.get_default_timezone())
    
    return dt

def load_csv_to_db(csv_file_path):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Iterate through the rows in the DataFrame and save to the database
    for index, row in df.iterrows():
        try:
            # Convert string timestamps to datetime objects
            timestamp = parse_timestamp(row['timestamp'])
            fire_start_time = parse_timestamp(row['fire_start_time'])
            
            # Parse latitude and longitude as floats
            latitude = float(row['latitude'])
            longitude = float(row['longitude'])

            # Create the FireEvent object
            fire_event = CurrentFireEvents(
                timestamp=timestamp,
                fire_start_time=fire_start_time,
                latitude=latitude,
                longitude=longitude,
                severity=row['severity']
            )

            # Save the record to the database
            fire_event.save()

        except Exception as e:
            print(f"Error processing row {index}: {e}")

# Specify the path to your CSV file
csv_file_path = "C:\\Users\\Mahmu\\Downloads\\drive-download-20250201T162900Z-001\\ConUHacks 2025 - codebase\\current_wildfiredata.csv"
load_csv_to_db(csv_file_path)