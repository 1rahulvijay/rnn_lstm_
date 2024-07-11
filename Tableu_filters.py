import requests

# Replace these variables with your Tableau Server details
username = 'your-username'
password = 'your-password'
server_url = 'https://your-tableau-server'
site_id = 'your-site-id'  # Use empty string "" for the default site
view_id = 'your-view-id'

# Authenticate and get a session token
auth_url = f"{server_url}/api/3.11/auth/signin"
auth_payload = {
    "credentials": {
        "name": username,
        "password": password,
        "site": {
            "contentUrl": site_id
        }
    }
}

auth_response = requests.post(auth_url, json=auth_payload)
auth_response.raise_for_status()  # Raise an exception for HTTP errors
auth_token = auth_response.json()['credentials']['token']
site_id = auth_response.json()['credentials']['site']['id']
headers = {
    'X-Tableau-Auth': auth_token
}

# Get the view details
view_url = f"{server_url}/api/3.11/sites/{site_id}/views/{view_id}"
view_response = requests.get(view_url, headers=headers)
view_response.raise_for_status()
view_details = view_response.json()

# Print view details
print(view_details)

# Get the filters for the view
filters_url = f"{server_url}/api/3.11/sites/{site_id}/views/{view_id}/filters"
filters_response = requests.get(filters_url, headers=headers)
filters_response.raise_for_status()
filters_details = filters_response.json()

# Print filters details
print(filters_details)

# Generate a CSV of the view's data
data_url = f"{server_url}/api/3.11/sites/{site_id}/views/{view_id}/data"
data_params = {
    'format': 'csv'
}
data_response = requests.get(data_url, headers=headers, params=data_params)
data_response.raise_for_status()

# Save the CSV to a file
csv_filename = 'view_data.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
    file.write(data_response.text)

print(f"Data exported to {csv_filename}")

# Sign out to invalidate the token
signout_url = f"{server_url}/api/3.11/auth/signout"
signout_response = requests.post(signout_url, headers=headers)
signout_response.raise_for_status()
