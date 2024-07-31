import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# Function to filter and split dataframe based on provided values and filenames
def filter_and_save_excel(df, split_column, include_values=None, exclude_values=None, filenames=None):
    if include_values is None:
        include_values = df[split_column].unique()
    if exclude_values is None:
        exclude_values = []
    if filenames is None:
        filenames = [f"{value}.xlsx" for value in include_values]

    filtered_values = set(include_values) - set(exclude_values)
    file_paths = []
    
    # Ensure filenames list is the same length as filtered values
    if len(filenames) < len(filtered_values):
        raise ValueError("Not enough filenames provided for the filtered values.")

    for i, value in enumerate(filtered_values):
        if value in df[split_column].unique():
            df_split = df[df[split_column] == value]
            file_path = filenames[i]
            df_split.to_excel(file_path, index=False)
            file_paths.append((file_path, value))
    
    return file_paths

# Function to send email with attachment
def send_email_with_attachment(to_email, subject, body, file_path, from_email, password):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach the file
    with open(file_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename={file_path}")
        msg.attach(part)
    
    # Set up the SMTP server
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())

# Example usage
df = pd.DataFrame({
    'split_column': ['A', 'B', 'A', 'B', 'C', 'A'],
    'data': [1, 2, 3, 4, 5, 6]
})

split_column = 'split_column'
include_values = ['A', 'B', 'C']  # Values to include in the split
exclude_values = []  # Values to exclude from the split
filenames = ['data_A.xlsx', 'data_B.xlsx', 'data_C.xlsx']  # Dynamic filenames

file_paths = filter_and_save_excel(df, split_column, include_values, exclude_values, filenames)

# Define mapping using a dictionary (value, email)
email_mapping = {
    'A': 'emailA@example.com',
    'B': 'emailB@example.com',
    'C': 'emailC@example.com'
}

from_email = 'your_email@example.com'
password = 'your_email_password'

for file_path, value in file_paths:
    to_email = email_mapping.get(value)
    if to_email:
        send_email_with_attachment(
            to_email,
            f"Data for {value}",
            f"Please find attached the data for {value}.",
            file_path,
            from_email,
            password
        )
