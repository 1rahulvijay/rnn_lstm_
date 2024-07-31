import tableauserverclient as TSC

# Tableau Server details
server_url = 'https://your-tableau-server.com'
username = 'your-username'
password = 'your-password'
site_id = 'your-site-id'  # use '' if you are not using any site

# Data source or workbook details
datasource_name = 'your-datasource-name'

# Sign in to Tableau Server
tableau_auth = TSC.TableauAuth(username, password, site_id)
server = TSC.Server(server_url, use_server_version=True)

with server.auth.sign_in(tableau_auth):
    # Get all data sources
    all_datasources, pagination_item = server.datasources.get()
    
    # Find the specific data source
    datasource = next((ds for ds in all_datasources if ds.name == datasource_name), None)
    
    if datasource is not None:
        # Get the refresh task for the data source
        req_option = TSC.RequestOptions()
        req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name, TSC.RequestOptions.Operator.Equals, datasource.name))
        
        all_tasks, pagination_item = server.tasks.get(req_option)
        
        # Filter extract refresh tasks
        extract_refresh_tasks = [task for task in all_tasks if isinstance(task, TSC.ScheduleItem) and task.task_type == 'ExtractRefresh']
        
        if extract_refresh_tasks:
            # Get the latest extract refresh task
            latest_task = max(extract_refresh_tasks, key=lambda task: task.updated_at)
            print(f"Latest refresh date for datasource '{datasource_name}': {latest_task.updated_at}")
        else:
            print(f"No extract refresh tasks found for datasource '{datasource_name}'")
    else:
        print(f"Datasource '{datasource_name}' not found")
