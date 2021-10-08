from django.urls import path
from django.http import HttpResponse

from api_input.views import (
    AddCallDetailedRecord
)

urlpatterns = [
    path('api/call_details_record/', AddCallDetailedRecord.as_view(), name='create-cdr'),
]