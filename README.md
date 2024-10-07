# Datasets Loader

The Datasets Loader is a tool designed to automatically process, generate mock data for, and distribute datasets across datasites. This project streamlines the handling of static datasets, making them easily accessible for testing and development purposes.

## Features

- Automatic schema generation for CSV and JSON files
- Mock data creation based on original data structure
- Distribution of processed datasets to owner's datasite
- Preservation of data privacy by excluding original data from distribution

## Project Structure

```
datasets_loader/
├── static_datasets/
│   ├── dataset_1/
│   │   ├── assets/
│   │   │   ├── file1.csv
│   │   │   ├── file2.json
│   │   │   └── contributors.csv
│   │   └── README.md
│   └── dataset_2/
│       └── ...
├── etl/
│   ├── csv/
│   │   └── main_csv.py
│   └── json/
│       └── main_json.py
├── main_1_day.py
└── README.md
```

## How to Use

1.
