from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, models
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from main.models import CallDetailRecord, CountedCallDetailRecord, Employee
from .serializers import CallDetailedRecordsSerializer


class AddCallDetailedRecord(CreateAPIView):
    queryset = CallDetailRecord.objects.all()
    serializer_class = CallDetailedRecordsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            print(str(e))
            return Response(f'Status Fail, uniq_id={serializer.data["uniqueid"]}', status=400)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(f'Status Ok, unique_id={serializer.data["uniqueid"]}', status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        try:
            serializer.create(serializer.validated_data)

        except IntegrityError as e:
            raise ValidationError(
                f'Status Fail, unique_id={serializer.validated_data["uniqueid"]}'
            )
