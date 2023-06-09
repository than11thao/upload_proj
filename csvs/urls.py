from .views import upload_file_view
from django.urls import path

app_name = 'csvs'

urlpatterns = [
    path('', upload_file_view, name='upload-view')
]
