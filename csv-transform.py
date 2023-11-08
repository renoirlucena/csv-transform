import csv

def load_ddd_data(file_path):
    """
    Loads the DDD data from a CSV file and returns a dictionary with the city-state tuple as the key and the DDD as the value.
    :param file_path: str
    :return: dict
    """
    ddd_dict = {}
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader, None)  # Read the header row
        headers = [h.strip() for h in headers]  # Strip spaces from header names
        for row in csv.DictReader(file, fieldnames=headers):
            # Create a tuple of city and state as key, and DDD as the value
            ddd_dict[(row['city'].strip().lower(), row['state'].strip().upper())] = row['ddd'].strip()
    return ddd_dict

def process_cellular(number, city, state, ddd_dict):
    """
    Processes the cellular number to ensure it has the correct DDD prefix based on the city and state, if necessary.
    :param number: str
    :param city: str
    :param state: str
    :param ddd_dict: dict
    :return: str
    """
    # Check if DDD is missing and add it if necessary
    if len(number) == 9:
        city_state_tuple = (city.strip().lower(), state.strip().upper())
        ddd = ddd_dict.get(city_state_tuple)
        if ddd:
            return f'{ddd}{number}'
    return number

def transform_csv(input_path, output_path, ddd_data_path):
    """
    Transforms the input CSV file to add missing DDDs to phone numbers and saves the result to the output path.
    :param input_path: str
    :param output_path: str
    :param ddd_data_path: str
    """
    # Load DDD data
    ddd_dict = load_ddd_data(ddd_data_path)

    with open(input_path, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_path, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['mobile', 'firstName', 'lastName', 'displayName']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()

        for row in reader:
            # Process cellular number
            processed_cellular = process_cellular(row['customer_cellular'], row['customer_city'], row['customer_state'], ddd_dict)
            # Write the transformed data
            writer.writerow({
                'mobile': processed_cellular,
                'firstName': row['first_name'].strip(),
                'lastName': row['last_name'].strip(),
                'displayName': f"{row['first_name'].strip()} {row['last_name'].strip()}"
            })

if __name__ == "__main__":
    # Define paths to the files
    input_csv_path = '/Users/renoirlucena/code/csv-transform/crm_export.csv'
    output_csv_path = '/Users/renoirlucena/code/csv-transform/processed_crm_export.csv'  # Name the output file as processed_crm_export.csv
    ddd_csv_path = '/Users/renoirlucena/code/csv-transform/ddd_data.csv'

    # Run the transformation
    transform_csv(input_csv_path, output_csv_path, ddd_csv_path)
