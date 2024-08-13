import tableauserverclient as TSC

# Tableau Server or Tableau Online connection details
server_url = "https://your-tableau-server-url"
tableau_username = "your-username"
tableau_password = "your-password"
site_id = ""  # Empty string for the default site

# The View ID of the dashboard from which you want to extract data
view_id = "your-view-id"

# Create a Tableau Server Auth object
tableau_auth = TSC.TableauAuth(tableau_username, tableau_password, site_id)

# Create a server object
server = TSC.Server(server_url, use_server_version=True)

# Sign in to the server
with server.auth.sign_in(tableau_auth):
    print("Signed in to Tableau Server successfully!")
    
    # Get the view by ID
    try:
        dashboard_view = server.views.get_by_id(view_id)

        if dashboard_view:
            # Fetch the full underlying data for the view
            req_option = TSC.RequestOptions()

            # Pagination to handle large data sets
            all_rows = []
            page_num = 0

            while True:
                req_option.page_size = 1000  # Adjust page size as necessary
                req_option.page_number = page_num

                server.views.populate_csv(dashboard_view, req_options=req_option)
                data = dashboard_view.content.splitlines()

                if not data:
                    break

                all_rows.extend(data)

                if len(data) < req_option.page_size:
                    break

                page_num += 1

            # Optionally, save the full data to a file
            with open("full_dashboard_data.csv", "w") as f:
                f.write("\n".join(all_rows))

            print("Full data extracted and saved successfully!")
        else:
            print(f"View with ID '{view_id}' not found.")

    except Exception as e:
        print(f"An error occurred: {e}")
