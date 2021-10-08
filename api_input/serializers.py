import uuid
from typing import Dict, Any

from rest_framework import serializers

from main.models import CallDetailRecord, CountedCallDetailRecord, Employee


class CallDetailedRecordsSerializer(serializers.Serializer):
    OutboundCID = serializers.CharField(allow_blank=True, required=False)
    src = serializers.CharField()
    dst = serializers.CharField()
    diversion = serializers.CharField(allow_blank=True, required=False)
    channel = serializers.CharField()
    dstchannel = serializers.CharField()
    start = serializers.DateTimeField()
    answer = serializers.DateTimeField(required=False, default=None, allow_null=True)
    end = serializers.DateTimeField(required=False, default=None, allow_null=True)
    duration = serializers.IntegerField(required=False, default=0)
    billsec = serializers.IntegerField(required=False, default=0)
    disposition = serializers.CharField()
    uniqueid = serializers.CharField()
    pbx = serializers.CharField(allow_blank=True)

    def to_internal_value(self, data):
        if data.get('answer') == '':
            data['answer'] = None

        if data.get('end') == '':
            data['end'] = None

        if data.get('billsec') == '':
            data['billsec'] = 0

        if data.get('duration') == '':
            data['duration'] = 0

        return super().to_internal_value(data)

    def create(self, validated_data: Dict[str, Any]):
        dst_phone = validated_data['dst']
        dst_channel = validated_data['dstchannel']
        bill_sec = validated_data['billsec']

        # price = self._calculate_price

        CountedCallDetailRecord.objects.create(
            outbound_cid=validated_data['OutboundCID'],
            src=validated_data['src'],
            dst=dst_phone,
            diversion=validated_data['diversion'],
            channel=validated_data['channel'],
            dst_channel=dst_channel,
            start=validated_data['start'],
            answer=validated_data['answer'],
            end=validated_data['end'],
            duration=validated_data['duration'],
            billsec=validated_data['billsec'],
            disposition=validated_data['disposition'],
            uniquie_id=validated_data['uniqueid'],
            pbx=validated_data['pbx'],
            id=uuid.uuid4(),
            # price=price,
        )

        CallDetailRecord.objects.create(
            outbound_cid=validated_data['OutboundCID'],
            src=validated_data['src'],
            dst=validated_data['dst'],
            diversion=validated_data['diversion'],
            channel=validated_data['channel'],
            dst_channel=validated_data['dstchannel'],
            start=validated_data['start'],
            answer=validated_data['answer'],
            end=validated_data['end'],
            duration=validated_data['duration'],
            billsec=validated_data['billsec'],
            disposition=validated_data['disposition'],
            uniquie_id=validated_data['uniqueid'],
            pbx=validated_data['pbx'],
            id=uuid.uuid4(),
        )

    # def _calculate_price(self):
    #     return

    class Meta:
        model = CallDetailRecord
        exclude = ['id']