from django.urls import path
from importCsv.views import csv_import, csv_setting

# url patterns for urls which starts with /import/
urlpatterns = [
    path('setting/', csv_setting, name='setting-csv'),
    path('csv/', csv_import, name='import-csv'),
]
