import csv
import re

def load_ddd_data(ddd_data_path):
    ddd_dict = {}
    with open(ddd_data_path, mode='r', encoding='utf-8') as ddd_file:
        ddd_reader = csv.DictReader(ddd_file, delimiter=',')
        ddd_reader.fieldnames = [name.strip() for name in ddd_reader.fieldnames]  # Clean header names
        for row in ddd_reader:
            key = (row['city'].strip().lower(), row['state'].strip().upper())
            ddd_dict[key] = row['ddd'].strip()
    return ddd_dict

def format_phone_number(phone, ddd_dict, city, state):
    phone = re.sub(r'\D', '', phone)  # Remove non-digit characters
    if len(phone) == 9 and phone.startswith('9'):
        key = (city.lower(), state.upper())
        ddd = ddd_dict.get(key, '')
        phone = '55' + ddd + phone
    return phone

def format_name(name):
    if not name:  # Check if the name is None or empty string
        return ''
    return ' '.join(word.capitalize() for word in name.split())


def transform_csv(input_csv_path, output_csv_path, ddd_data_path):
    ddd_dict = load_ddd_data(ddd_data_path)
    written_rows = set()  # Set to store unique identifiers of written rows

    with open(input_csv_path, mode='r', encoding='utf-8') as infile, \
         open(output_csv_path, mode='w', encoding='utf-8', newline='') as outfile:

        reader = csv.DictReader(infile, delimiter=';')
        fieldnames = ['mobile', 'firstname', 'lastname', 'display_name']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()

        for row in reader:
            phone = row.get('customer_cellular', '').strip()

            # If there's no phone number or if the phone number is already written, skip the row
            if not phone or phone in written_rows:
                continue

            formatted_row = {}  # Create a new dictionary for the formatted data

            # Format the name and create display name
            firstname = format_name(row.get('customer_name', ''))
            lastname = format_name(row.get('customer_lastname', ''))
            formatted_row['firstname'] = firstname
            formatted_row['lastname'] = lastname
            formatted_row['display_name'] = firstname + ' ' + lastname

            # Format phone numbers
            city = row.get('customer_city', '')
            state = row.get('customer_state', '')
            formatted_phone = format_phone_number(phone, ddd_dict, city, state)

            # If the formatted phone is already in written_rows, skip the row
            if formatted_phone in written_rows:
                continue

            formatted_row['mobile'] = formatted_phone

            # Add the phone to the set of written rows
            written_rows.add(formatted_phone)

            writer.writerow(formatted_row)

# Paths to the data
input_csv_path = 'data/input_data.csv'
output_csv_path = 'data/output_data.csv'
ddd_data_path = 'data/ddd_data.csv'

# Run the CSV transformation
transform_csv(input_csv_path, output_csv_path, ddd_data_path)
