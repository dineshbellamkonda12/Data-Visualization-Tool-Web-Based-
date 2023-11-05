# views.py
from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.db.models.functions import TruncYear
from .models import RainfallData
import json

def visualize_data(request):
    aggregated_data = RainfallData.objects.all().values('date').annotate(total_rainfall=Sum('rainfall'))

    aggregated_data_by_month = (
        RainfallData.objects.annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total_rainfall=Sum('rainfall'))
    )

    aggregated_data_by_year = (
        RainfallData.objects.annotate(year=TruncYear('date'))
        .values('year')
        .annotate(total_rainfall=Sum('rainfall'))
    )

    dates = [entry['date'].strftime("%Y-%m-%d %H:%M:%S") for entry in aggregated_data]
    rainfall_values = [entry['total_rainfall'] for entry in aggregated_data]

    months = [entry['month'].strftime("%Y-%m") for entry in aggregated_data_by_month]
    rainfall_values_by_month = [entry['total_rainfall'] for entry in aggregated_data_by_month]

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
