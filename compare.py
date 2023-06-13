import pandas as pd

 

def compare_csv_files(csv1_path, csv2_path):
    # Read the CSV files into pandas DataFrames
    df1 = pd.read_csv(csv1_path)
    df2 = pd.read_csv(csv2_path)

 

    # Find rows from df1 that do not exist in df2
    missing_rows = []

 

    for index, row in df1.iterrows():
        matching_rows = df2[df2.eq(row)].dropna()
        if matching_rows.empty:
            missing_rows.append(row)

 

    return pd.DataFrame(missing_rows)

 

# Specify the file paths for the CSV files
csv1_path = 'data_format.csv'
csv2_path = 'dataformat2.csv'

 

# Call the function to compare the CSV files
result = compare_csv_files(csv1_path, csv2_path)

 

# Print the missing rows
if result.empty:
    print("All rows from csv1 exist in csv2.")
else:
    print("Rows from csv1 that do not exist in csv2:")
    for index, row in result.iterrows():
        print("Row:", row.values)


