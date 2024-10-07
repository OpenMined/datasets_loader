import json
import argparse
from collections import defaultdict
import datetime
import random
import lorem

MAX_DEPTH = 10  # Maximum depth for nested structures

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
    ]
    for fmt, desc in date_formats:
        try:
            datetime.datetime.strptime(string, fmt)
            return f"date ({desc})"
        except ValueError:
            pass
    return None

def analyze_json_structure(data, prefix='', depth=0):
    if depth > MAX_DEPTH:
        return {prefix: "string (deeply nested)"}

    schema = {}
    if isinstance(data, dict):
        for key, value in data.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            schema.update(analyze_json_structure(value, new_prefix, depth + 1))
    elif isinstance(data, list):
        if data:
            schema[prefix] = "array"
            sample = data[:10] + data[-10:] if len(data) > 20 else data
            for item in sample:
                item_schema = analyze_json_structure(item, prefix, depth + 1)
                for k, v in item_schema.items():
                    if k not in schema:
                        schema[k] = v
                    elif schema[k] != v:
                        schema[k] = f"mixed ({schema[k]}, {v})"
    else:
        if isinstance(data, str):
            date_type = is_date(data)
            if date_type:
                schema[prefix] = date_type
            else:
                schema[prefix] = "string"
        elif isinstance(data, bool):
            schema[prefix] = "boolean"
        elif isinstance(data, int):
            schema[prefix] = "integer"
        elif isinstance(data, float):
            schema[prefix] = "number"
        elif data is None:
            schema[prefix] = "null"
        else:
            schema[prefix] = type(data).__name__
    return schema

def count_occurrences(data):
    counts = defaultdict(int)
    null_counts = defaultdict(int)
    
    def traverse(obj, prefix=''):
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_prefix = f"{prefix}.{key}" if prefix else key
                counts[new_prefix] += 1
                if value is None or (isinstance(value, (list, dict)) and not value):
                    null_counts[new_prefix] += 1
                traverse(value, new_prefix)
        elif isinstance(obj, list):
            counts[prefix] += len(obj)
            for item in obj:
                traverse(item, prefix)
        else:
            counts[prefix] += 1
    
    traverse(data)
    return counts, null_counts

def generate_schema_description(schema, counts, null_counts, input_filename):
    description = f"Schema for {input_filename}\n\n"
    for key, value_type in schema.items():
        if key.startswith('[].'):
            key = key[3:]  # Remove the '[].' prefix
        description += f"Field: {key}\n"
        if null_counts[key] > 0:
            value_type = f"nullable {value_type}"
        description += f"Type: {value_type}\n"
        description += f"Occurrences: {counts[key]}\n"
        if null_counts[key] > 0:
            description += f"Null/Empty Occurrences: {null_counts[key]}\n"
            description += f"Optional: Yes\n"
        else:
            description += f"Optional: No\n"
        description += "\n"
    return description

def parse_schema_file(schema_file):
    schema = {}
    total_items = 1  # Default to 1 if not specified
    with open(schema_file, 'r') as f:
        lines = f.readlines()
        current_field = None
        for line in lines:
            line = line.strip()
            if line.startswith('Field:'):
                current_field = line.split('Field:')[1].strip()
                schema[current_field] = {}
            elif line.startswith('Type:') and current_field:
                type_info = line.split('Type:')[1].strip()
                if type_info.startswith('nullable'):
                    schema[current_field]['type'] = type_info.split()[1]
                    schema[current_field]['nullable'] = True
                else:
                    schema[current_field]['type'] = type_info
                    schema[current_field]['nullable'] = False
            elif line.startswith('Occurrences:') and current_field:
                occurrences = int(line.split('Occurrences:')[1].strip())
                schema[current_field]['occurrences'] = occurrences
                total_items = max(total_items, occurrences)
            elif line.startswith('Optional:') and current_field:
                schema[current_field]['optional'] = line.split('Optional:')[1].strip().lower() == 'yes'
    return schema, total_items

def generate_mock_value(type_='string', nullable=False, optional=False):
    if optional and random.random() < 0.2:  # 20% chance of null for optional fields
        return None
    if nullable and random.random() < 0.1:  # 10% chance of null for nullable fields
        return None
    if type_ == 'integer':
        return random.randint(0, 1000)
    elif type_ == 'number':
        return round(random.uniform(0, 1000), 2)
    elif type_ == 'boolean':
        return random.choice([True, False])
    elif type_.startswith('date'):
        return generate_mock_date(type_)
    elif type_ == 'string':
        return lorem.sentence()[:50]  # Limit string length
    elif type_ == 'null':
        return None
    else:
        return lorem.sentence()[:50]  # Default to string if type is unknown

def generate_mock_date(date_format):
    base = datetime.datetime.now()
    date = base - datetime.timedelta(days=random.randint(0, 365*5))  # Random date within last 5 years
    if 'datetime' in date_format.lower():
        return date.strftime('%Y-%m-%d %H:%M:%S')
    elif 'DD/MM/YYYY' in date_format:
        return date.strftime('%d/%m/%Y')
    elif 'MM/DD/YYYY' in date_format:
        return date.strftime('%m/%d/%Y')
    elif 'YYYY/MM/DD' in date_format:
        return date.strftime('%Y/%m/%d')
    elif 'DD-MM-YYYY' in date_format:
        return date.strftime('%d-%m-%Y')
    elif 'MM-DD-YYYY' in date_format:
        return date.strftime('%m-%d-%Y')
    elif 'YYYY.MM.DD' in date_format:
        return date.strftime('%Y.%m.%d')
    elif 'DD.MM.YYYY' in date_format:
        return date.strftime('%d.%m.%Y')
    elif 'MM.DD.YYYY' in date_format:
        return date.strftime('%m.%d.%Y')
    elif 'MM/DD/YY' in date_format:
        return date.strftime('%m/%d/%y')
    else:
        return date.strftime('%Y-%m-%d')  # Default format

def generate_mock_json(schema, total_items):
    result = []
    for _ in range(total_items):
        item = {}
        for field, info in schema.items():
            item[field] = generate_mock_value(
                info.get('type', 'string'),
                info.get('nullable', False),
                info.get('optional', False)
            )
        result.append(item)
    return result

def main(input_filepath, output_filepath):
    with open(input_filepath, 'r') as f:
        data = json.load(f)
    
    schema = analyze_json_structure(data)
    counts, null_counts = count_occurrences(data)
    
    description = generate_schema_description(schema, counts, null_counts, input_filepath)
    
    with open(output_filepath, 'w') as f:
        f.write(description)
    
    print(f"Schema description has been written to {output_filepath}")

def generate_mock_json_file(schema_file, output_file):
    schema, total_items = parse_schema_file(schema_file)
    mock_data = generate_mock_json(schema, total_items)
    with open(output_file, 'w') as f:
        json.dump(mock_data, f, indent=2)
    print(f"Mock JSON data generated: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate schema description for a nested JSON file.')
    parser.add_argument('input', help='Path to the input JSON file')
    parser.add_argument('output', help='Path to the output schema description file')
    args = parser.parse_args()

    main(args.input, args.output)