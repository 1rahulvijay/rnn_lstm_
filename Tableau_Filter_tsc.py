import pandas as pd
import io
import tableauserverclient as TSC

def download_data(view_id, filters):
    with server.auth.sign_in(tableau_auth):
        # Fetch the view
        view = server.views.get_by_id(view_id)
        if view is None:
            raise ValueError(f"No view found with ID: {view_id}")
        print(f"View details: {view}")

        # Initialize CSV request options
        csv_req_option = TSC.CSVRequestOptions(max_age=5)

        # Apply multiple filters
        for filter_name, filter_values in filters.items():
            for value in filter_values:
                csv_req_option.vf(filter_name, value)

        # Retrieve the CSV data for the view
        server.views.populate_csv(view, csv_req_option)
        
        # Combine chunks of CSV data into a single string
        csv_data = "".join([chunk.decode("utf-8") for chunk in view.csv])

        # Read CSV data into a DataFrame
        df = pd.read_csv(io.StringIO(csv_data))
        
    return df
