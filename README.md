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

1. **Adding a New Dataset**:
   - Create a new folder in `static_datasets/` with your dataset name.
   - Inside this folder, create an `assets/` directory.
   - For each dataset asset, create a folder like `asset_0/`.
   - Place your original CSV or JSON files in the `asset_X/` directory.
   - Add a `contributors.csv` file in the `assets/` directory.
   - Create a `README.md` file in the dataset's root folder describing the dataset.

2. **Running the Loader**:
   - The loader runs automatically as part of the daily task.
   - To manually trigger the process, run:
     ```
     python main_1_day.py
     ```

3. **What the Loader Does**:
   - Generates schema files (`*_schema.txt`) for each data file.
   - Creates mock data files (`*_mock.csv` or `*_mock.json`).
   - Copies processed files (excluding original data) to the owner's datasite.

4. **Accessing Processed Data**:
   - After processing, find the mock data and schema files in:
     ```
     <owner_datasite>/datasets/mock/<dataset_name>/
     ```

5. **Updating Existing Datasets**:
   - Replace or modify files in the `static_datasets/` directory.
   - Re-run the loader to update processed files.

## Best Practices

- Keep original data files in their native format (CSV or JSON).
- Regularly update the `contributors.csv` files to credit all contributors.
- Provide comprehensive information in each dataset's `README.md` file.
- Set `REPLACE_ALL = True` in `main_1_day.py` to regenerate all files (use cautiously).

## Privacy and Security

- Original data files are never copied to the owner's datasite.
- Only mock data, schema files, and metadata are distributed.
- Ensure you have the right to use and share the data you add to the loader.

## Troubleshooting

- If schema or mock files are not generating, check file permissions and formats.
- For issues with data distribution, verify the `client_config.json` file is correctly set up.

## Contributing

To contribute to the Datasets Loader project:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a clear description of your changes.

For any questions or support, please contact the development team.
