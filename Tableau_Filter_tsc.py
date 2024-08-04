import tableauserverclient as TSC
import pandas as pd
from datetime import datetime
import urllib.parse

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

            # Construct the URL with filters
            filter_query = '&'.join([f'vf_{urllib.parse.quote(key)}={urllib.parse.quote(value)}' for key, value in filters.items()])
            csv_url = f"{self.server.baseurl}/views/{view.id}/data?{filter_query}"

            # Get the filtered data
            response = self.server._make_request('GET', csv_url)
            csv_data = response.content.decode('utf-8')

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
