from app.models import Order, Position, Watchlist
from app.orders.market import market_order
from settings.timing import market_open
from celery import shared_task
from django_celery_results.models import TaskResult
from app.watchlist.price_stream import update_data2


@shared_task
def limit_orders():
    from app.symbols.details import get_price

    orders = Order.objects.filter(status='pending', type='LIMIT').iterator()
    for order in orders:
        if not market_open(order.segment):
            return 'Market Closed'

        try:
            current_price = float(get_price(order.symbol))
            if (
                (order.order_type == 'BUY' and current_price <= float(order.price)) or
                (order.order_type == 'SELL' and current_price >= float(order.price))
            ):
                m_user = order.user
                m_symbol = order.symbol
                m_quantity = order.quantity
                m_order_type = order.order_type
                m_product = order.product
                m_stoploss = order.stoploss
                m_target = order.target
                m_type = order.type
                order.delete()
                market_order(
                    m_user, m_symbol, m_quantity, m_order_type,
                    m_product, m_stoploss, m_target, m_type
                )
        except Exception as e:
            continue
    return True


@shared_task
def delete_results():
    TaskResult.objects.all().delete()
    return 'Tasks Deleted Successfully'


# @shared_task
# def stoploss_target():
#     from app.symbols.details import get_price

#     positions = Position.objects.filter(is_closed=False).iterator()
#     for position in positions:
#         if float(position.stoploss) == 0.0:
#             continue

#         if not market_open(position.segment):
#             return 'Market Closed'

#         try:
#             current_price = float(get_price(position.symbol))

#             if (
#                 (position.quantity > 1 and (current_price <= float(position.stoploss) or current_price >= float(position.target))) or
#                 (position.quantity < 1 and (current_price >= float(position.stoploss) or current_price <= float(position.target)))
#             ):
#                 order_type = 'BUY' if position.quantity > 1 else 'SELL'
#                 market_order(
#                     position.user, position.symbol, abs(position.quantity), order_type,
#                     position.product, 0, 0, 'MARKET'
#                 )
#         except Exception as e:
#             continue
#     return True


@shared_task
def close_positions_mcx():
    positions = Position.objects.filter(is_closed=False, is_holding=False, segment='MCX').iterator()
    for position in positions:
        order_type = 'BUY' if position.quantity > 1 else 'SELL'
        market_order(
            position.user, position.symbol, abs(position.quantity), order_type,
            position.product, 0, 0, 'MARKET'
        )
    return 'Positions Closed'


@shared_task
def close_positions_nse():
    positions = Position.objects.filter(is_closed=False, is_holding=False).exclude(segment='MCX').iterator()
    for position in positions:
        order_type = 'BUY' if position.quantity > 1 else 'SELL'
        market_order(
            position.user, position.symbol, abs(position.quantity), order_type,
            position.product, 0, 0, 'MARKET'
        )
    return 'Positions Closed'


@shared_task
def update_watchlist():
    watchlist = Watchlist.objects.all()
    symbol_list = [item.stock for item in watchlist]
    data = update_data2(symbol_list)

    for item in watchlist:
        item.price = data['data'][item.stock]['ltp']
        item.open = data['data'][item.stock]['open']
        item.close = data['data'][item.stock]['close']
        item.high = data['data'][item.stock]['high']
        item.low = data['data'][item.stock]['low']
        item.save()

    return {'status': 'success', 'message': 'Watchlist Updated'}