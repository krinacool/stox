from wallet.calculation import add_amount, deduct_amount
from django.utils import timezone

# POSITION LOGIC
def scalp_position_open(user,instrument_key,product):
    from app.models import Position
    today = timezone.now().date()
    if product == 'INTRADAY':
        pos = Position.objects.filter(user=user,instrument_key=instrument_key,product=product,created_at__date=today)
    else:
        pos = Position.objects.filter(user=user,instrument_key=instrument_key,product=product)
    if pos.exists():
        pos = pos.first()
        if pos.quantity < 0:
            return True
        else:
            return False
    else:
        return False

def position_open(user,instrument_key,product):
    from app.models import Position
    today = timezone.now().date()
    if product == 'INTRADAY':
        pos = Position.objects.filter(user=user,instrument_key=instrument_key,product=product,created_at__date=today)
    else:
        pos = Position.objects.filter(user=user,instrument_key=instrument_key,product=product)
    if pos.exists():
        pos = pos.first()
        if pos.quantity > 0:
            return True
        else:
            return False
    else:
        return False

def get_position(user,instrument_key,product,new=False):
    from app.models import Position
    today = timezone.now().date()
    pos = ''
    if product == 'CARRYFORWARD':
        if new:
            pos = None
        else:
            pos = Position.objects.filter(user=user,instrument_key=instrument_key,product=product,is_closed=False).first()
    else:
        pos = Position.objects.filter(user=user,instrument_key=instrument_key,product=product,created_at__date=today).first()
    return pos

def createPosition(user,instrument_key,quantity,ordertype,product,price,stoploss,target):
    print('create positions')
    from app.models import Position
    pos = get_position(user,instrument_key,product,new=True)
    if pos is None:
        qty = quantity
        if ordertype == 'SELL':
            qty = quantity * -1
        pos = Position.objects.create(
            user = user,
            quantity = qty,
            instrument_key = instrument_key,
            product = product,
            )
    else:
        pos.buy_price=0
        pos.sell_price=0
        if ordertype == 'BUY':
            pos.quantity = quantity
        else:
            pos.quantity = quantity * -1
            pos.save()

    if ordertype == 'BUY':
        pos.buy_price = price
    else:
        pos.sell_price = price
        pos.security_amount = (price * quantity) + ((price * quantity) / 2)
        deduct_amount(user,pos.security_amount)
    pos.stoploss = stoploss
    pos.target = target
    pos.save()


def close_full_position(user,instrument_key,product,price):
    pos = get_position(user,instrument_key,product)
    pos.last_traded_quantity = pos.quantity
    pos.quantity = 0
    if position_open(user,instrument_key,product):
        pos.sell_price = price
        pos.save()
    if scalp_position_open(user,instrument_key,product):
        pos.buy_price = price
        add_amount(user,pos.security_amount)
        pos.security_amount = 0
        pnl = (pos.sell_price - pos.buy_price) * pos.last_traded_quantity
        add_amount(user,pnl)
        pos.save()

def add_more_position(user,instrument_key,quantity,product,price,stoploss,target):
    pos = get_position(user,instrument_key,product)
    if position_open(user,instrument_key,product):
        pos.quantity = pos.quantity + quantity
        pos.buy_price = (pos.buy_price + price) / 2
        pos.stoploss = stoploss
        pos.target = target
        pos.save()
    if scalp_position_open(user,instrument_key,product):
        pos.quantity = pos.quantity + (pos.quantity * -1)
        pos.sell_price = (pos.buy_price + price) / 2
        pos.security_amount = pos.security_amount + ((price * quantity) / 2)
        pos.stoploss = stoploss
        pos.target = target
        deduct_amount(user,((price * quantity) + ((price * quantity) / 2)))
        pos.save()


def close_some_position(user,instrument_key,quantity,product,price):
    pos = get_position(user,instrument_key,product)
    pos.last_traded_quantity = quantity
    if position_open(user,instrument_key,product):
        pos.quantity = pos.quantity - quantity
        pos.sell_price = price
        pos.save()
    if scalp_position_open(user,instrument_key,product):
        pos.quantity = pos.quantity - (quantity * -1)
        pos.buy_price = price
        # pos.security_amount = pos.security_amount - (price * quantity)
        pnl = (pos.sell_price - pos.buy_price ) * (quantity * -1)
        add_amount(user,pnl)
        pos.save()