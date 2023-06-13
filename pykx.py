import logging
import pykx as kx
import pandas as pd
from datetime import date
import boto3
import os

# Configure logging
logging.basicConfig(filename='query.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def compare_xlsx_with_s3(hostname, port, s3_bucket, s3_key):
    conn = None
    try:
        # Establish a connection to the kdb+ server
        conn = kx.QConnection(hostname, port)
        logging.info(f"Connected to kdb+ server at {hostname}:{port}")
        
        # Get the current date as a string
        current_date = date.today().strftime('%Y.%m.%d')
        
        # Construct the query string with the current date
        query = f'''
        dt: {current_date};
        status: 2_key .enum.operationalStatus;
        res: .kxs.getSensors[(`hdr`orgID`filter`params`columns!(()!();1i;"deviceType=`METER,installDate<=.api.p.dt";enlist[`dt]!enlist[dt];`kxsLocation.locID`kxsSensor.serialNo`extSensorID`extSmpID`kxsSMP.grp`deviceOperationalStatus`installDate`provState`updateTS))];
        tmp: select count i by date: dt, provState: provState, OperationalStatus: .enum.operationalStatus?deviceOperationalStatus from res 1;
        '''
        
        # Execute the query
        conn(query)
        
        # Retrieve the result and format it as a DataFrame
        result = conn('''tmp''').pd()
        result.columns = ['provState', 'OperationalStatus', 'Count']
        
        # Save the result as an XLSX file
        output_file = 'output.xlsx'
        result.to_excel(output_file, index=False)
        logging.info(f"XLSX file '{output_file}' created successfully.")
        
        # Read the XLSX file from S3
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=s3_bucket, Key=s3_key)
        s3_xlsx = pd.read_excel(io.BytesIO(response['Body'].read()),header=3)
        
        # Merge the result DataFrame with the S3 DataFrame on 'provState' column
        merged_df = pd.merge(result, s3_xlsx, on='State')
        
        # Compare the rows for each column
        for column in merged_df.columns[1:]:
            mismatch_rows = merged_df[merged_df[column + '_x'] != merged_df[column + '_y']]
            if not mismatch_rows.empty:
                logging.info(f"Mismatch found in column '{column}':")
                logging.info(mismatch_rows)
            else:
                logging.info(f"No mismatch found in column '{column}'.")
        
    except Exception as e:
        logging.error(f"Error: {e}")
        
    finally:
        if conn is not None:
            conn.close()

# Set the hostname, port, S3 bucket, and S3 key
hostname = "172.12.12.45"
port = 12202
s3_bucket = 'your-s3-bucket'
s3_key = 's3file.xlsx'

# Call the function to execute the query and compare the XLSX files
compare_xlsx_with_s3(hostname, port, s3_bucket, s3_key)
