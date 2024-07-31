from rest_framework import serializers
from app.models import Position

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        exclude = ['id', 'position_id', 'stoploss', 'target', 'security_amount', 'user']


class HoldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        exclude = ['id', 'position_id', 'stoploss', 'target', 'security_amount', 'user']
