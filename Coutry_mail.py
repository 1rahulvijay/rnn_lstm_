import win32com.client as win32
import pandas as pd
import tableauserverclient as TSC
import io

class ReportingAutomation:
    def __init__(self, email_dict, tableau_auth, server_url):
        self.email_dict = email_dict
        self.tableau_auth = tableau_auth
        self.server = TSC.Server(server_url, use_server_version=True)

    def send_email(self, df):
        for country, email in self.email_dict.items():
            country_data = df[df["Country Name"] == country]

            if not country_data.empty:
                subject = f"Data for {country}"
                body = f"{country} data:\n\n{country_data.to_string(index=False)}"

                outlook = win32.Dispatch("outlook.application")
                mail = outlook.CreateItem(0)
                mail.To = email
                mail.Subject = subject
                mail.Body = body

                mail.Display()
                print(f"Email sent to {email}")
            else:
                print(f"No data found for {country}")

        return df

    def retrieve_tableau_data(self, view_id):
        with self.server.auth.sign_in(self.tableau_auth):
            try:
                view = self.server.views.get_by_id(view_id)
                if view is None:
                    raise ValueError(f"No view found with ID: {view_id}")

                csv_data = "--".join([chunk.decode("utf-8") for chunk in view.csv()])
                csv_data_io = io.StringIO(csv_data)
                df = pd.read_csv(csv_data_io)
                return df

            except TSC.ServerResponseError as e:
                print(f"Server error: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    email_dict = {'Country1': 'email1@example.com', 'Country2': 'email2@example.com'}
    tableau_auth = TSC.PersonalAccessTokenAuth('name', 'token', 'site')
    server_url = 'your_server_url'

    automation = ReportingAutomation(email_dict, tableau_auth, server_url)
    df = automation.retrieve_tableau_data('view_id')
    automation.send_email(df)
