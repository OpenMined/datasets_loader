import os
import shutil
from pathlib import Path
from syftbox.lib import ClientConfig

# Import the main functions from the ETL scripts
from etl.csv.main_csv import main as process_csv, generate_mock_csv
from etl.json.main_json import main as process_json, generate_mock_json_file

# Set this to True if you want to delete all existing schema and mock files before generating new ones
REPLACE_ALL = True

# Set up the basic configuration
app_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
client_config = ClientConfig.load(os.path.expanduser("~/.syftbox/client_config.json"))

def process_file(file_path):
    # Skip processing if the file is already a mock or schema file
    if '_mock' in file_path.name or '_schema' in file_path.name:
        print(f"Skipping mock or schema file: {file_path}")
        return None

    output_file = file_path.with_name(f"{file_path.stem}_schema.txt")
    
    if output_file.exists():
        print(f"Schema file already exists: {output_file}")
        return output_file

    if file_path.suffix == '.csv':
        process_csv(str(file_path), str(output_file))
    elif file_path.suffix == '.json':
        process_json(str(file_path), str(output_file))
    else:
        print(f"Unsupported file type: {file_path}")
        return None

    print(f"Schema description written to: {output_file}")
    return output_file

def delete_schemas_and_mocks(root_path):
    for file in root_path.rglob('*_schema.txt'):
        print(f"Deleting schema file: {file}")
        file.unlink()
    
    for file in root_path.rglob('*_mock.json'):
        print(f"Deleting mock JSON file: {file}")
        file.unlink()
    
    for file in root_path.rglob('*_mock.csv'):
        print(f"Deleting mock CSV file: {file}")
        file.unlink()

def cleanup_incorrect_mocks(root_path):
    for file in root_path.rglob('*_mock_mock*'):
        print(f"Removing incorrect mock file: {file}")
        file.unlink()
    
    for file in root_path.rglob('*_schema_mock*'):
        print(f"Removing incorrect mock file: {file}")
        file.unlink()

    for file in root_path.rglob('*_mock_schema*'):
        print(f"Removing incorrect schema file: {file}")
        file.unlink()

def copy_dataset_to_datasite(dataset_folder, owner_datasite):
    target_folder = owner_datasite / 'datasets' / 'mock' / dataset_folder.name
    target_folder.mkdir(parents=True, exist_ok=True)

    for item in dataset_folder.rglob('*'):
        if item.is_file():
            # Skip the original data files
            if not (item.name.endswith('_mock.csv') or item.name.endswith('_mock.json') or 
                    item.name.endswith('_schema.txt') or item.name == 'contributors.csv' or 
                    item.name == 'README.md'):
                continue
            
            relative_path = item.relative_to(dataset_folder)
            target_file = target_folder / relative_path
            
            # Remove '_mock' from the filename if it's a mock file
            if '_mock' in target_file.name:
                target_file = target_file.with_name(target_file.name.replace('_mock', ''))
            
            target_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target_file)

def daily_task():
    print("Performing daily task: Generating schema descriptors and mock data for datasets...")
    
    static_datasets_path = Path(__file__).parent / 'static_datasets'
    
    if REPLACE_ALL:
        print("REPLACE_ALL flag is set. Deleting all existing schema and mock files...")
        delete_schemas_and_mocks(static_datasets_path)
    
    for dataset_folder in static_datasets_path.iterdir():
        if dataset_folder.is_dir():
            for assets_folder in (dataset_folder / "assets").iterdir():
                for file in assets_folder.iterdir():
                    if file.name != 'contributors.csv' and file.suffix in ['.csv', '.json']:
                        print(f"Processing file: {file}")
                        schema_file = process_file(file)
                        if schema_file:
                            mock_file = file.with_name(f"{file.stem}_mock{file.suffix}")
                            
                            if file.suffix == '.csv':
                                generate_mock_csv(schema_file, mock_file)
                            elif file.suffix == '.json':
                                generate_mock_json_file(schema_file, mock_file)

    cleanup_incorrect_mocks(static_datasets_path)
    
    # Copy datasets to owner's datasite
    owner_datasite = Path(client_config.datasite_path)
    for dataset_folder in static_datasets_path.iterdir():
        if dataset_folder.is_dir():
            print(f"Copying dataset {dataset_folder.name} to owner's datasite...")
            copy_dataset_to_datasite(dataset_folder, owner_datasite)
    
    print("Daily task completed.")

if __name__ == "__main__":
    daily_task()

# Congratulations! You've set up a daily task in your SyftBox application.
# Remember:
# - This script is called by run.sh once a day (see section_3 in run.sh)
# - It also runs when the program first starts
# - You can add any Python code here that you want to execute on this schedule
# - Consider using the pipeline folders (input, running, done) in your daily tasks

# Next steps:
# 1. Test your implementation by running this script directly
# 2. Check the output in your SyftBox logs to ensure it's working as expected
# 3. Consider how this daily task interacts with other parts of your application
# 4. Proceed to requirements.txt to complete the tutorial

# Happy coding!