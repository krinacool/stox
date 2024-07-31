from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render,redirect
from app.models import Instrument
from settings.timing import market_open
from app.orders.market import market_order
from app.orders.limit import initiate_limit_order
from django.utils.timezone import localdate
from app.models import Position
from api.serializers import *

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):
    if request.method == 'POST':
        instrument_key = request.data.get("instrument")
        price = request.data.get("price")
        quantity = request.data.get("quantity")
        order_type = request.data.get("order_type")
        product = request.data.get("product_type")
        type = request.data.get("type")
        stoploss = request.data.get("stoploss", "0")  # Default to "0" if not provided
        target = request.data.get("target", "0")  # Default to "0" if not provided

        # Validate mandatory fields
        if not all([instrument_key, price, quantity, order_type, product, type]):
            return Response({'error': 'All mandatory fields must be provided'}, status=400)

        # Convert types and validate
        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            return Response({'error': 'Invalid price or quantity'}, status=400)

        if quantity <= 0:
            return Response({'error': 'Quantity must be greater than zero'}, status=400)

        order_type = order_type.upper()
        if order_type not in ["BUY", "SELL"]:
            return Response({'error': 'Order type must be either BUY or SELL'}, status=400)

        product = product.capitalize()
        if product not in ["Intraday", "Carryforward"]:
            return Response({'error': 'Product type must be either Intraday or Carryforward'}, status=400)

        type = type.capitalize()
        if type not in ["Market", "Limit"]:
            return Response({'error': 'Type must be either Market or Limit'}, status=400)

        og = Instrument.objects.filter(instrument_key=instrument_key).first()
        if not og:
            return Response({'error': 'Instrument not found'}, status=404)

        segment = og.exchange
        symbol = og.tradingsymbol
        token = og.exchange_token

        if not market_open(segment):
            return Response({'error': 'Market is closed'}, status=400)

        quantity = quantity * og.lot_size

        if type == 'Market':
            status = market_order(request.user, symbol, instrument_key, token, quantity, order_type, product, stoploss, target, 'Market')
        else:
            status = initiate_limit_order(request.user, symbol, instrument_key, token, price, quantity, order_type, product, stoploss, target)

        if status == "failed":
            return Response({'error': 'Order Rejected'}, status=400)
        else:
            return Response({'message': 'Order placed successfully'})
    else:
        return Response({'error': 'Method not allowed'}, status=405)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_positions(request):
    today = localdate()
    positions = Position.objects.filter(user=request.user, last_traded_datetime__date=today)
    serializer = PositionSerializer(positions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_holdings(request):
    today = localdate()
    positions = Position.objects.filter(user=request.user,is_holding=True,is_closed=False).exclude(created_at__date=today)
    serializer = HoldingSerializer(positions, many=True)
    return Response(serializer.data)

def documentation(request):
    return render(request,"home/documentation.html")

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

token_obtain_pair_view = CustomTokenObtainPairView.as_view()
