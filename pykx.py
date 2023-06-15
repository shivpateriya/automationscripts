# Import the datetime module
from datetime import datetime

# ...

def compare_xlsx_with_s3(hostname, port, s3_bucket, s3_key):
    conn = None
    try:
        # Establish a connection to the kdb+ server
        conn = kx.QConnection(hostname, port)
        logging.info(f"Connected to kdb+ server at {hostname}:{port}")

        # Get the current date as a string in the desired format
        current_date = datetime.today().strftime('%m/%d/%Y')  # Format: MM/DD/YYYY

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
        result.columns = ['State', 'Operational Status', 'Count']
        result['Date'] = current_date  # Add the current date column

        # Save the result as an XLSX file
        output_file = 'output.xlsx'
        result.to_excel(output_file, index=False)
        logging.info(f"XLSX file '{output_file}' created successfully.")

        # Read the XLSX file from S3
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=s3_bucket, Key=s3_key)
        s3_xlsx = pd.read_excel(response['Body'])

        # Iterate over each state and operational status in the result DataFrame
        for _, row in result.iterrows():
            state = row['State']
            operational_status = row['Operational Status']
            count = row['Count']

            # Check if the corresponding data exists in the S3 XLSX file
            matching_row = s3_xlsx[(s3_xlsx['state'] == state) & (s3_xlsx['Opertional Status'] == operational_status) & (s3_xlsx['Count'] == count)]

            # Print the result
            if matching_row.empty:
                logging.info(f"No match found for State: {state}, Operational Status: {operational_status}, Count: {count}")
            else:
                logging.info(f"Match found for State: {state}, Operational Status: {operational_status}, Count: {count}")

    except Exception as e:
        logging.error(f"Error: {e}")

    finally:
        if conn is not None:
            conn.close()
