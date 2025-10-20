# data-worker
Data Worker Functionality 
  SummaryThe purpose of the "data worker" is to asynchronously process heavy data analysis tasks in the background that would otherwise block the web application.The entire system operates in the following flow:
  1. Components and General FlowComponentRole in the FlowDjango ServerReceives the user's request (the CSV file and email address).views.pySaves the file temporarily and immediately delegates the heavy work to the Celery Worker.RabbitMQActs as the Broker, receiving and holding the task in the queue until the Worker requests it.Celery Worker (process_data_analysis)Executes the task, reads the file, simulates the intensive analysis (time.sleep(15)), and performs Pandas calculations.PandasIs used within the Celery task to perform the actual data analysis (e.g., counting rows, calculating the average of the 'value_column').Email BackendSends an email notification to the user upon task completion, reporting the result.
  2. Specific Task Execution Flow (process_data_analysis)
  The core task, defined in analytics.tasks.process_data_analysis, performs the following steps once executed by Celery:

  File Reading: Reads the uploaded CSV file (whose path was passed as an argument) using Pandas (pd.read_csv(file_path)).

  Load Simulation: Simulates a lengthy, heavy process using time.sleep(15).

  Data Analysis: Executes the real data analysis, which includes:

  Counting the total number of records (total_rows = len(data)).

  Calculating the average value of a specific column (average_value = data['value_column'].mean()).

  Performing a more complex analysis, such as grouping and finding the region with the highest sales (top_region = data.groupby('region')).

  User Notification: Sends an email to the user (using the Console EMAIL_BACKEND for debugging) notifying that the analysis is complete and including the analysis result.

    To run client , use:
  >> celery -A core worker -l info --pool=solo
  
    To run server , use:
  >> python manage.py runserver