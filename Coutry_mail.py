import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_country_data(df_values, df_mails, default_email):
    # Ensure the dataframes have the necessary columns
    if 'country_name' not in df_values.columns or 'value' not in df_values.columns:
        raise ValueError("df_values must contain 'country_name' and 'value' columns")
    if 'country_name' not in df_mails.columns or 'mail' not in df_mails.columns:
        raise ValueError("df_mails must contain 'country_name' and 'mail' columns")

    # Create a dictionary from df_mails for quick lookup
    email_dict = df_mails.set_index('country_name')['mail'].to_dict()

    # Iterate over each country in df_values
    for country, group in df_values.groupby('country_name'):
        # Get the email address from the dictionary or use the default email
        email = email_dict.get(country, default_email)
        
        # Convert the country_data to a string
        country_data_str = group.to_string(index=False)
        
        # Create the email content
        subject = f"Data for {country}"
        body = f"Please find the data for {country} below:\n\n{country_data_str}"
        msg = MIMEMultipart()
        msg['From'] = 'your_email@example.com'  # Replace with your email
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # Send the email
        try:
            with smtplib.SMTP('smtp.example.com', 587) as server:  # Replace with your SMTP server and port
                server.starttls()
                server.login('your_email@example.com', 'your_password')  # Replace with your login credentials
                server.sendmail(msg['From'], msg['To'], msg.as_string())
                print(f"Email sent to {email} for {country}")
        except Exception as e:
            print(f"Failed to send email to {email} for {country}: {e}")

# Example usage:
# Default email address for countries not found in df_mails
default_email = 'default@abc.com'

# Load your dataframes from the Excel file
df_values = pd.read_excel('data.xlsx', sheet_name='Values')
df_mails = pd.read_excel('data.xlsx', sheet_name='Mails')

send_country_data(df_values, df_mails, default_email)
