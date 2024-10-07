# Static Datasets

This folder is designed to store various static datasets for use in our applications. It provides a standardized structure for organizing and documenting datasets, making them easy to manage and use across different projects.

## Dataset Structure Tutorial

Follow these steps to create a new dataset:

1. Create a new folder with your dataset name:
   ```
   my_dataset/
   ```

2. Inside this folder, create an `assets` directory:
   ```
   my_dataset/
   └── assets/
   ```

3. For each distinct data asset, create a subfolder in `assets`:
   ```
   my_dataset/
   └── assets/
       ├── asset_1/
       └── asset_2/
   ```

4. In each asset folder, include:
   - The original data file (CSV or JSON format)
   - A `contributors.csv` file
   - A `README.md` file
   ```
   my_dataset/
   └── assets/
       └── asset_1/
           ├── original_data.csv
           ├── contributors.csv
           └── README.md
   ```

5. Add a `contributors.csv` file in the root of your dataset folder:
   ```
   my_dataset/
   ├── assets/
   └── contributors.csv
   ```

## Automatic File Generation

Our system will automatically generate the following files for each data asset:

- `*_schema.txt`: A description of the data structure
- `*_mock.csv` or `*_mock.json`: Mock data based on the original file's schema

Do not create these files manually, as they will be overwritten by the automatic process.

## Best Practices

1. Use clear, descriptive names for your dataset and asset folders.
2. Provide comprehensive information in each asset's README.md file, including:
   - Dataset description
   - Data sources
   - File descriptions
   - Any usage notes or caveats
3. Keep original data files in their native format (CSV or JSON).
4. Regularly update the contributors.csv files to credit all contributors.
5. Respect data privacy and ensure you have the right to use and share the data.

## contributors.csv Format

Use the following format for contributors.csv files: