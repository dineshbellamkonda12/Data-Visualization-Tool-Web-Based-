import os
from datetime import datetime
import openpyxl

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stanpro.settings")
import django

django.setup()

# Import the RainfallData model after configuring the settings
from stanapp.models import RainfallData

xlsx_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'xlsx_files', 'rainfalldata.xlsx')

workbook = openpyxl.load_workbook(xlsx_file_path)
sheet = workbook.active

for row in sheet.iter_rows(min_row=2, values_only=True):
    date_value = row[0]
    if isinstance(date_value, datetime):
        date_value = date_value.strftime('%d/%m/%Y %H:%M')
    RainfallData.objects.create(
        date=datetime.strptime(date_value, '%d/%m/%Y %H:%M'),
        rainfall=float(row[1])
    )