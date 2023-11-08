import csv

# A function to process the cellular number based on the DDD data
def process_cellular(cellular, city, state, ddd_data):
    # If the cellular number is already in the correct format, return it as is
    if len(cellular) in [11, 12]:  # Assuming phone numbers should be 11 or 12 digits long
        return cellular

    # Find the DDD for the given city and state
    for ddd_entry in ddd_data:
        if ddd_entry['City'].strip().lower() == city.strip().lower() and ddd_entry['State'].strip().lower() == state.strip().lower():
            return f"({ddd_entry['DDD']}){cellular}"

    # If no DDD is found, return the original cellular number
    return cellular

# Load the DDD data
with open('ddd_data.csv', mode='r', encoding='utf-8') as ddd_file:
    ddd_reader = csv.DictReader(ddd_file)
    ddd_data = list(ddd_reader)

# Process the CRM CSV file
with open('crm_export.csv', mode='r', encoding='utf-8') as crm_file:
    crm_reader = csv.DictReader(crm_file)

    # Prepare the new CSV file
    with open('processed_customers.csv', mode='w', newline='', encoding='utf-8') as outfile:
        fieldnames = ['mobile', 'firstName', 'lastName', 'displayName']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        # Process each row
        for row in crm_reader:
            processed_cellular = process_cellular(row['customer_cellular'], row['customer_city'], row['customer_state'], ddd_data)
            writer.writerow({
                'mobile': processed_cellular,
                'firstName': row['first_name'],
                'lastName': row['last_name'],
                'displayName': f"{row['first_name']} {row['last_name']}"
            })

print("Processing complete. The file processed_customers.csv has been created.")
