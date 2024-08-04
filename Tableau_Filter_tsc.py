import tableauserverclient as TSC
import pandas as pd
from datetime import datetime

class TableauDataDownloader:
    def __init__(self, token_name, token_value, site_id, server_url):
        self.tableau_auth = TSC.PersonalAccessTokenAuth(
            token_name=token_name,
            personal_access_token=token_value,
            site_id=site_id
        )
        self.server = TSC.Server(server_url, use_server_version=True)

    def connect(self):
        self.server.auth.sign_in(self.tableau_auth)

    def disconnect(self):
        self.server.auth.sign_out()

    def download_data(self, workbook_name, view_name, filters, output_file='output.csv'):
        with self.server.auth.sign_in(self.tableau_auth):
            # Get the workbook and the specific view
            all_workbooks, pagination_item = self.server.workbooks.get()
            workbook = next((wb for wb in all_workbooks if wb.name == workbook_name), None)

            if workbook is None:
                raise Exception('Workbook not found')

            self.server.workbooks.populate_views(workbook)
            view = next((v for v in workbook.views if v.name == view_name), None)

            if view is None:
                raise Exception('View not found')

            # Apply filters to the view
            for filter_name, filter_value in filters.items():
                self.server.views.apply_filter(view, filter_name, filter_value, TSC.FilterOperator.Equals)

            # Get filtered data from the view
            csv_req_option = TSC.CSVRequestOptions()
            csv_data = self.server.views.populate_csv(view, csv_req_option)

            # Save the CSV data to a file
            with open(output_file, 'w') as file:
                file.write(csv_data)

            # Optionally, load into a pandas DataFrame for further processing
            df = pd.read_csv(output_file)
            print(df.head())
            return df

# Example usage
if __name__ == "__main__":
    token_name = 'your_token_name'
    token_value = 'your_token_value'
    site_id = 'your_site_id'  # Leave empty for default site
    server_url = 'https://your-tableau-server-url'

    downloader = TableauDataDownloader(token_name, token_value, site_id, server_url)
    filters = {
        'Cluster': 'NAM',
        'Region': 'US',
        'Date': datetime.today().strftime('%Y-%m-%d'),
        'Name': 'Rahul'
    }
    
    downloader.download_data('your_workbook_name', 'your_view_name', filters)
