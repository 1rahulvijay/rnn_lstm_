import pandas as pd
import win32com.client as win32

# Step 1: Create a sample DataFrame and dictionary
data = {
    'country_name': ['India', 'USA', 'Germany'],
    'money': ['100 USD', '200 USD', '300 USD']
}
df = pd.DataFrame(data)

email_dict = {"India": "india@outlook.com", "USA": "usa@example.com", "Germany": "germany@example.com"}

# Step 2: Define a function to locate data and send an email
def send_email(df, email_dict):
    # Loop through the dictionary
    for country, email in email_dict.items():
        # Locate the data in the DataFrame
        country_data = df[df['country_name'] == country]
        
        if not country_data.empty:
            # Prepare the email content
            subject = f"Financial Report for {country}"
            body = f"Dear {country} Team,\n\nHere is the financial report for {country}:\n\n{country_data.to_string(index=False)}\n\nBest regards,\nFinance Team"
            
            # Send the email using win32com
            outlook = win32.Dispatch('outlook.application')
            mail = outlook.CreateItem(0)
            mail.To = email
            mail.Subject = subject
            mail.Body = body
            
            # For sending email with an attachment
            # attachment_path = "path_to_attachment"
            # mail.Attachments.Add(attachment_path)
            
            mail.Send()
            print(f"Email sent to {email}")
        else:
            print(f"No data found for {country}")
    
    return df

# Step 3: Call the function to send the email and return the DataFrame
updated_df = send_email(df, email_dict)
print(updated_df)
