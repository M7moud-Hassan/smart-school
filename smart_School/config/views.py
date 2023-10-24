import copy
import csv
import sqlite3
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
content_message=[]
def result_files(request):
     temp=copy.deepcopy(content_message)
     content_message.clear()
     return JsonResponse({'strings': temp})
def add_files(request):
    content_message = []  # Initialize the content_message list

    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            content_message.append('Start uploading file ' + uploaded_file.name)
            if not uploaded_file.name.endswith('.csv'):
                content_message.append('Only CSV files are allowed.')
                return HttpResponseBadRequest('Only CSV files are allowed.')
            else:
                try:
                    # Read and process the CSV file
                    data = []
                    with uploaded_file:
                        reader = csv.reader(uploaded_file)
                        for row in reader:
                            data.append(row)
                            content_message.append(row)
                    # Process 'data' as needed
                    content_message.append(f'Successfully processed {len(data)} rows from {uploaded_file.name}')
                except FileNotFoundError:
                    content_message.append("The CSV file was not found.")
                except Exception as e:
                    content_message.append(f"An error occurred: {str(e)}")
            content_message.append('Exit')

    return render(request, 'config/add_files.html')