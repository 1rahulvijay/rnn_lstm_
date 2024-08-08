# Get the list of workbooks available to the authenticated user
all_workbooks, pagination_item = server.workbooks.get()

# Optionally, filter workbooks by name
workbook_name = "Your Workbook Name"
workbook = next((wb for wb in all_workbooks if wb.name == workbook_name), None)

if workbook:
    # Get details of the workbook
    server.workbooks.populate_views(workbook)

    # Loop through views to find your specific dashboard view
    dashboard_name = "Your Dashboard Name"
    dashboard_view = next((v for v in workbook.views if v.name == dashboard_name), None)

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
        print(f"Dashboard '{dashboard_name}' not found in workbook '{workbook_name}'.")
else:
    print(f"Workbook '{workbook_name}' not found.")
