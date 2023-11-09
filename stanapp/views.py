# views.py
from django.shortcuts import render
from django.db.models import Sum
from django.http import JsonResponse
from django.db.models.functions import TruncMonth
from django.db.models.functions import TruncYear
from .models import RainfallData
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import json
import numpy as np
import pandas as pd
import joblib
from datetime import datetime

# Function for visualizing aggregated rainfall data for different time periods
def visualize_data(request):
    # Retrieve aggregated data for all entries
    aggregated_data = RainfallData.objects.all().values('date').annotate(total_rainfall=Sum('rainfall'))

    # Retrieve aggregated data by month
    aggregated_data_by_month = (
        RainfallData.objects.annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total_rainfall=Sum('rainfall'))
    )

    # Retrieve aggregated data by year
    aggregated_data_by_year = (
        RainfallData.objects.annotate(year=TruncYear('date'))
        .values('year')
        .annotate(total_rainfall=Sum('rainfall'))
    )

    # Extract dates and rainfall values for plotting
    dates = [entry['date'].strftime("%Y-%m-%d %H:%M:%S") for entry in aggregated_data]
    rainfall_values = [entry['total_rainfall'] for entry in aggregated_data]

    # Extract months and related rainfall values for plotting
    months = [entry['month'].strftime("%Y-%m") for entry in aggregated_data_by_month]
    rainfall_values_by_month = [entry['total_rainfall'] for entry in aggregated_data_by_month]

    # Extract years and related rainfall values for plotting
    years = [entry['year'].strftime("%Y") for entry in aggregated_data_by_year]
    rainfall_values_by_year = [entry['total_rainfall'] for entry in aggregated_data_by_year]

    context = {
        'dates': json.dumps(dates),
        'rainfall_values': json.dumps(rainfall_values),
        'months': json.dumps(months),
        'rainfall_values_by_month': json.dumps(rainfall_values_by_month),
        'years': json.dumps(years),
        'rainfall_values_by_year': json.dumps(rainfall_values_by_year)
    }

    return render(request, 'visualize_data.html', context)

# Function for training a linear regression model on the rainfall data and saving it to a file
def train_model_and_save():
    data = RainfallData.objects.all()
    dates = np.array([entry.date.timestamp() for entry in data])
    rainfalls = np.array([entry.rainfall for entry in data])

    # Reshape the dates array
    dates = dates.reshape(-1, 1)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(dates, rainfalls, test_size=0.2, random_state=42)

    # Create a Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train, X_test, y_test)

    # Save the trained model to a file
    joblib.dump(model, 'rainfall_model.pkl')

# Function for predicting the rainfall within a specific date range
def predict_range(request):
    if request.method == 'POST':
        try:
            model = joblib.load('rainfall_model.pkl')
        except FileNotFoundError:
            train_model_and_save()
            model = joblib.load('rainfall_model.pkl')

        # Extract start_date and end_date from the request
        start_date_str = request.POST.get('start_date', None)
        end_date_str = request.POST.get('end_date', None)

        # Convert the date strings to datetime objects
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d %H:%M')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d %H:%M')

        # Create a date range based on the start and end dates
        dates = pd.date_range(start=start_date, end=end_date, freq='H')
        predictions = []

        # Aggregate data by day and make predictions
        aggregated_data = {}
        for date in dates:
            prediction = model.predict(np.array(date.timestamp()).reshape(-1, 1))
            date_key = date.strftime('%Y-%m-%d')
            if date_key not in aggregated_data:
                aggregated_data[date_key] = []
            aggregated_data[date_key].append(prediction.tolist()[0])

        for date, values in aggregated_data.items():
            average_value = sum(values) / len(values)
            predictions.append({'date': date, 'prediction': average_value})

        return JsonResponse({'predictions': predictions})
    else:
        return render(request, 'prediction_template.html')
    
# A simple view that renders a custom data visualization template
def empty_view(request):
    return render(request, 'custom_data_visualize.html')
