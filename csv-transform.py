import csv

# Define file paths for input and output
csv_file_path = 'crm_export.csv'  # Replace with actual customer data CSV file name
ddd_data_path = 'ddd_data.csv'  # DDD data CSV file

# Function to load DDD data into a dictionary
def load_ddd_data(file_path):
    ddd_dict = {}
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Create a key as a tuple of city and state for direct lookup
            ddd_dict[(row['city'].strip(), row['state'].strip())] = row['ddd'].strip()
    return ddd_dict

# Function to update cellular numbers with missing DDD
def process_cellular(cell_number, city, state, ddd_dict):
    # Clean up any formatting in the cell number
    clean_number = cell_number.replace(' ', '').replace('-', '')

    # Check for missing DDD by length of the cell number
    if len(clean_number) < 11:
        ddd_key = (city, state)
        # Prepend missing DDD if city and state match in ddd_dict
        if ddd_key in ddd_dict:
            clean_number = ddd_dict[ddd_key] + clean_number
        else:
            # Log an error or handle cases with missing DDD information
            print(f"Warning: No DDD found for {city}, {state}")
    return clean_number

# Load DDD data from provided CSV
ddd_dict = load_ddd_data(ddd_data_path)

# Initialize a list to hold processed records
processed_records = []

# Read customer data and process cellular numbers
with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        row['customer_cellular'] = process_cellular(
            row.get('customer_cellular', ''),
            row.get('customer_city', ''),
            row.get('customer_state', ''),
            ddd_dict
        )
        processed_records.append(row)

# Define path for the output CSV file
output_csv_path = 'processed_customer_data.csv'

# Write processed data to a new CSV file
with open(output_csv_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=processed_records[0].keys())
    writer.writeheader()
    writer.writerows(processed_records)

print(f"Data processing complete. Output saved to {output_csv_path}")
