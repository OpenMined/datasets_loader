import csv
import os
import datetime
from collections import defaultdict
import json
import argparse
import random
import lorem

def is_date(string):
    date_formats = [
        ("%Y-%m-%d", "ISO8601 date"),
        ("%d/%m/%Y", "DD/MM/YYYY"),
        ("%m/%d/%Y", "MM/DD/YYYY"),
        ("%Y/%m/%d", "YYYY/MM/DD"),
        ("%d-%m-%Y", "DD-MM-YYYY"),
        ("%m-%d-%Y", "MM-DD-YYYY"),
        ("%Y.%m.%d", "YYYY.MM.DD"),
        ("%d.%m.%Y", "DD.MM.YYYY"),
        ("%m.%d.%Y", "MM.DD.YYYY"),
        ("%Y-%m-%dT%H:%M:%S", "ISO8601 datetime"),
        ("%Y-%m-%d %H:%M:%S", "YYYY-MM-DD HH:MM:SS"),
        ("%m/%d/%y", "MM/DD/YY"),  # Add this line for the Netflix format
    ]
    for fmt, desc in date_formats:
        try:
            datetime.datetime.strptime(string, fmt)
            return desc
        except ValueError:
            pass
    return None

def analyze_csv(filepath):
    schema = {}
    with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        
        for header in headers:
            schema[header] = {
                'type': 'unknown',
                'unique_values': 0,
                'null_count': 0,
                'max_length': 0,
                'date_format': None
            }
        
        row_count = 0
        for row in reader:
            row_count += 1
            for i, value in enumerate(row):
                header = headers[i]
                if value.strip() == '':
                    schema[header]['null_count'] += 1
                    continue
                
                schema[header]['max_length'] = max(schema[header]['max_length'], len(value))
                
                if schema[header]['type'] == 'unknown':
                    date_format = is_date(value)
                    if date_format:
                        schema[header]['type'] = 'date'
                        schema[header]['date_format'] = date_format
                    elif value.replace('.', '').isdigit():
                        schema[header]['type'] = 'numeric'
                    else:
                        schema[header]['type'] = 'string'
                elif schema[header]['type'] == 'date':
                    # Ensure all values in the column are dates
                    if not is_date(value):
                        schema[header]['type'] = 'string'
                        schema[header]['date_format'] = None
        
        for header in headers:
            schema[header]['unique_values'] = len(set(row[headers.index(header)] for row in csv.reader(csvfile)))
    
    return schema, row_count

def generate_schema_description(schema, row_count, input_filename):
    description = f"Schema for {input_filename}\n"
    description += f"Total rows: {row_count}\n\n"
    
    for header, info in schema.items():
        description += f"Column: {header}\n"
        description += f"Type: {info['type']}\n"
        if info['type'] == 'date':
            description += f"Date Format: {info['date_format']}\n"
        description += f"Max Length: {info['max_length']}\n"
        description += f"Null Count: {info['null_count']}\n"
        description += f"Unique Values: {info['unique_values']}\n"
        description += "\n"
    
    return description

def parse_schema_file(schema_file):
    schema = {}
    total_rows = 0
    with open(schema_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("Total rows:"):
                total_rows = int(line.split(":")[1].strip())
            elif line.startswith("Column:"):
                current_column = line.split(":")[1].strip()
                schema[current_column] = {}
            elif line.startswith("Type:"):
                schema[current_column]['type'] = line.split(":")[1].strip()
            elif line.startswith("Date Format:"):
                schema[current_column]['date_format'] = line.split(":")[1].strip()
            elif line.startswith("Max Length:"):
                schema[current_column]['max_length'] = int(line.split(":")[1].strip())
    return schema, total_rows

def generate_mock_value(type_, date_format=None, max_length=None):
    if type_ == 'numeric':
        return random.randint(0, 1000)
    elif type_ == 'date':
        base = datetime.datetime.now()
        date = base - datetime.timedelta(days=random.randint(0, 365*5))
        if 'datetime' in date_format.lower():
            return date.strftime('%Y-%m-%d %H:%M:%S')
        elif 'DD/MM/YYYY' in date_format:
            return date.strftime('%d/%m/%Y')
        elif 'MM/DD/YYYY' in date_format:
            return date.strftime('%m/%d/%Y')
        elif 'YYYY/MM/DD' in date_format:
            return date.strftime('%Y/%m/%d')
        else:
            return date.strftime('%Y-%m-%d')
    else:
        return lorem.sentence()[:max_length]

def generate_mock_csv(schema_file, output_file):
    schema, total_rows = parse_schema_file(schema_file)
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=schema.keys())
        writer.writeheader()
        for _ in range(total_rows):
            row = {}
            for column, info in schema.items():
                row[column] = generate_mock_value(info['type'], info.get('date_format'), info.get('max_length'))
            writer.writerow(row)
    
    print(f"Mock CSV data generated: {output_file}")

def main(input_filepath, output_filepath):
    input_filename = os.path.basename(input_filepath)
    
    schema, row_count = analyze_csv(input_filepath)
    description = generate_schema_description(schema, row_count, input_filename)
    
    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write(description)
    
    print(f"Schema description has been written to {output_filepath}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate schema description for a CSV file.')
    parser.add_argument('input', help='Path to the input CSV file')
    parser.add_argument('output', help='Path to the output schema description file')
    args = parser.parse_args()

    main(args.input, args.output)