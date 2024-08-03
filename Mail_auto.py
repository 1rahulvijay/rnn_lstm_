import pandas as pd
import tableauserverclient as TSC
import io
import tempfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

class ReportingAutomation:
    def __init__(self, email_dict, tableau_auth, server_url, smtp_server, smtp_port, smtp_user, smtp_password):
        self.email_dict = email_dict
        self.tableau_auth = tableau_auth
        self.server = TSC.Server(server_url, use_server_version=True)
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password

    def send_email(self, df):
        for country, email in self.email_dict.items():
            country_data = df[df["Country Name"] == country]

            if not country_data.empty:
                subject = f"Data for {country}"
                body = f"Please find attached the data for {country}."

                # Save country_data to a temporary Excel file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                    country_data.to_excel(tmp.name, index=False, sheet_name=country)
                    tmp_path = tmp.name

                # Create the email
                msg = MIMEMultipart()
                msg['From'] = self.smtp_user
                msg['To'] = email
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))

                # Attach the Excel file
                with open(tmp_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {os.path.basename(tmp_path)}",
                    )
                    msg.attach(part)

                # Send the email
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.smtp_user, self.smtp_password)
                    server.sendmail(self.smtp_user, email, msg.as_string())
                print(f"Email sent to {email}")

                # Remove the temporary file
                os.remove(tmp_path)
            else:
                print(f"No data found for {country}")

        return df

    def retrieve_tableau_data(self, view_id):
        with self.server.auth.sign_in(self.tableau_auth):
            try:
                view = self.server.views.get_by_id(view_id)
                if view is None:
                    raise ValueError(f"No view found with ID: {view_id}")

                # Use the correct method to retrieve CSV data from the view
                self.server.views.populate_csv(view)
                csv_data = view.csv
                csv_data_io = io.StringIO(csv_data.decode("utf-8"))
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
    smtp_server = 'your_smtp_server'
    smtp_port = 587  # Typically 587 for TLS, 465 for SSL
    smtp_user = 'your_smtp_username'
    smtp_password = 'your_smtp_password'

    automation = ReportingAutomation(email_dict, tableau_auth, server_url, smtp_server, smtp_port, smtp_user, smtp_password)
    df = automation.retrieve_tableau_data('view_id')
    if df is not None:
        automation.send_email(df)
