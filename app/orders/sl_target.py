from app.symbols.details import get_price
from app.models import Position
import time
from app.orders.market import market_order


def stoploss_target(position_id):
    position = Position.objects.get(position_id=position_id)
    stoploss = position.stoploss
    target = position.target
    start_time = time.time()
    current_price = get_price(position.symbol)
    # while time.time() - start_time < 50400:
    while True:
        position = Position.objects.get(position_id=position_id)
        try:
            if position.stoploss != stoploss or position.target != target:
                return 'failed'
            if position.quantity == '0':
                return 'failed'
            elif position.quantity > 1:
                if (position.stoploss >= current_price or current_price >= position.target):
                    market_order(position.user,position.symbol,position.quantity,'SELL',position.product,0,0,'MARKET')
                    return 'success'
            else:
                if (position.stoploss <= current_price or current_price <= position.target):
                    market_order(position.user,position.symbol,position.quantity,'BUY',position.product,0,0,'MARKET')
                    return 'success'
            current_price = get_price(position.symbol)
        except Exception as e:
            return 'failed'

                