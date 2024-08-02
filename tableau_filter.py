import tableauserverclient as TSC
import pandas as pd
from datetime import datetime

# Define your Tableau Server credentials and connection details
tableau_auth = TSC.PersonalAccessTokenAuth(
    token_name='your_token_name',
    personal_access_token='your_token_value',
    site_id='your_site_id'  # Leave empty for default site
)
server = TSC.Server('https://your-tableau-server-url', use_server_version=True)

# Connect to Tableau Server
with server.auth.sign_in(tableau_auth):
    # Get the workbook and worksheet
    all_workbooks, pagination_item = server.workbooks.get()
    workbook = next((wb for wb in all_workbooks if wb.name == 'your_workbook_name'), None)

    if workbook is None:
        raise Exception('Workbook not found')

    server.workbooks.populate_views(workbook)
    worksheet = next((view for view in workbook.views if view.name == 'your_worksheet_name'), None)

    if worksheet is None:
        raise Exception('Worksheet not found')

    # Apply filters to the view
    req_option = TSC.RequestOptions()
    req_option.vf['Cluster'] = 'NAM'  # Apply the filter for 'Cluster' with value 'NAM'
    req_option.vf['Region'] = 'US'  # Apply the filter for 'Region' with value 'US'
    req_option.vf['Date'] = datetime.today().strftime('%Y-%m-%d')  # Apply the filter for 'Date' with today's date
    req_option.vf['Name'] = 'Rahul'  # Apply the filter for 'Name' with value 'Rahul'

    # Get filtered data
    server.views.populate_csv(worksheet, req_options=req_option)
    csv_data = worksheet.csv

    # Save the CSV data to a file
    with open('output.csv', 'w') as file:
        file.write(csv_data)

    # Optionally, load into a pandas DataFrame for further processing
    df = pd.read_csv('output.csv')
    print(df.head())
