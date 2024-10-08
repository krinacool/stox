from app.symbols.details import symbollist
from wallet.calculation import calc_carrage, wallet_checked
from app.models import Order
from app.orders.position_logic import scalp_position_open,position_open,get_position
import datetime
import time
import threading
from app.orders.market import market_order
from settings.models import nse_market_time, mcx_market_time
from app.symbols.details import get_price


# def limit_orderssss(user,symbol,price,quantity,order_type,product):
#     data = symbollist.get(symbol)
#     segment = data['segment']
#     markettime = nse_market_time.objects.first()
#     ordered = False
#     order = ""
#     total_amount = price * quantity
#     amount = total_amount + calc_carrage(total_amount,order_type)
#     if order_type == 'BUY':
#         if scalp_position_open(symbol,product):
#             order = Order.objects.create(user=user,symbol=symbol,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="initiated",type='LIMIT',stoploss=stoploss,target=target)
#         else:
#             if wallet_checked(user,amount):
#                 deduct_amount(user,amount)
#                 order = Order.objects.create(user=user,symbol=symbol,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="initiated",type='LIMIT',stoploss=stoploss,target=target)
#             else:
#                 order = Order.objects.create(user=user,symbol=symbol,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="failed",type='LIMIT',message='Insufficient Funds',stoploss=stoploss,target=target)
#                 return "failed"
#     else:
#         if position_open(symbol,product):
#             order = Order.objects.create(user=user,symbol=symbol,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="initiated",type='LIMIT',stoploss=stoploss,target=target)
#         else:
#             if wallet_checked(user,(amount/2)):
#                 deduct_amount(user,(amount/2))
#                 order = Order.objects.create(user=user,symbol=symbol,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="initiated",type='LIMIT',stoploss=stoploss,target=target)
#             else:
#                 order = Order.objects.create(user=user,symbol=symbol,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="failed",type='LIMIT',message='Insufficient Funds',stoploss=stoploss,target=target)
#                 return "failed"
#     current_time = str(datetime.datetime.now().strftime('%H:%M:%S'))
#     market = str(markettime.close_time.strftime('%H:%M:%S'))
#     while not ordered:
#         if (current_time ==  market):
#             break
#         current_price = get_price(symbol)
#         if (
#             (order_type == 'BUY' and current_price <= price) or
#             (order_type == 'SELL' and current_price >= price)
#         ):
#             new_amount = current_price * quantity
#             new_amount = calc_carrage(new_amount,order_type)
#             order.price = current_price
#             order.amount = new_amount
#             order.status = "completed"
#             order.save()
#             createPosition(user,symbol,quantity,order_type,product,current_price)# ==============
#             if order_type == "BUY":
#                 if scalp_position_open(symbol,product):
#                     deduct_amount(user,new_amount)
#                 else:
#                     add_amount(user,amount)
#                     deduct_amount(user,new_amount)
#             else:
#                 if position_open(symbol,product):
#                     add_amount(user,new_amount)
#                 else:
#                     pass
#             ordered = True
#             return "completed"
#         current_time = str(datetime.datetime.now().strftime('%H:%M:%S'))
#     add_amount(user,amount)
#     order.status = "failed"
#     order.save()
#     return "failed"





def place_limit_order(order_id,stoploss,target):
    print('Hello World')
    order = Order.objects.get(order_id=order_id)
    markettime = nse_market_time.objects.first()
    if order.segment == 'MCX':
        markettime = mcx_market_time.objects.first()
    ordered = False
    current_time = str(datetime.datetime.now().strftime('%H:%M:%S'))
    market = str(markettime.close_time.strftime('%H:%M:%S'))
    start_time = time.time()
    while not ordered and time.time() - start_time < 50400:
        order = Order.objects.get(order_id=order_id)
        try:
            if order.status == 'cancelled':
                return 'failed'
            if (current_time ==  market):
                order.status == 'failed'
                return 'failed'
            current_price = get_price(order.symbol)
            if (
                (order.order_type == 'BUY' and current_price <= order.price) or
                (order.order_type == 'SELL' and current_price >= order.price)
            ):
                market_order(order.user,order.symbol,order.quantity,order.order_type,order.product,stoploss,target,order.type)
                order.delete()
                return 'success'
        except:
            return 'failed'
        order.status == 'failed'
        order.save()
    return 'failed'

def limit_order(user,symbol,price,quantity,order_type,product,stoploss,target,type='LIMIT'):
    data = symbollist.get(symbol)
    segment = data['segment']
    amount = 0
    total_amount = price * quantity
    charges = calc_carrage(total_amount,order_type,product,user)
    pos = get_position(user,symbol,product)
    pos_quantity = 0
    if pos is not None:
        pos_quantity = pos.quantity
    if order_type == 'BUY':
        if scalp_position_open(user,symbol,product):
            pos_quantity = pos_quantity * -1
            if quantity > pos_quantity:
                new_quantity = quantity-pos_quantity
                amount = price * new_quantity
                if wallet_checked(user,amount,product):
                    order = Order.objects.create(user=user,symbol=symbol,segment=segment,price=price,amount=total_amount,quantity=quantity,order_type=order_type,product=product,status="pending",type=type,charges=0,stoploss=stoploss,target=target)
                    thread = threading.Thread(target=place_limit_order, args=(order.order_id,stoploss,target))
                    thread.start()
                else:
                    order = Order.objects.create(user=user,symbol=symbol,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="failed",type=type,charges=0,message='Insufficient Funds',stoploss=stoploss,target=target)
                    return 'failed'
            elif quantity < pos_quantity:
                order = Order.objects.create(user=user,symbol=symbol,segment=segment,price=price,amount=total_amount,quantity=quantity,order_type=order_type,product=product,status="pending",type=type,charges=charges,stoploss=stoploss,target=target)
                thread = threading.Thread(target=place_limit_order, args=(order.order_id,stoploss,target))
                thread.start()
            else:
                order = Order.objects.create(user=user,symbol=symbol,segment=segment,price=price,amount=total_amount,quantity=quantity,order_type=order_type,product=product,status="pending",type=type,charges=charges,stoploss=stoploss,target=target)
                thread = threading.Thread(target=place_limit_order, args=(order.order_id,stoploss,target))
                thread.start()
        # SCALP POSITION IS NOT OPEN
        else:
            if wallet_checked(user,total_amount,product):
                order = Order.objects.create(user=user,symbol=symbol,segment=segment,price=price,amount=total_amount,quantity=quantity,order_type=order_type,product=product,status="pending",type=type,charges=charges,stoploss=stoploss,target=target)
                thread = threading.Thread(target=place_limit_order, args=(order.order_id,stoploss,target))
                thread.start()
            else:
                order = Order.objects.create(user=user,symbol=symbol,segment=segment,price=price,amount=total_amount,quantity=quantity,order_type=order_type,product=product,status="failed",type=type,charges=0,message='Insufficient Funds',stoploss=stoploss,target=target)
                return 'failed'
    # SELL SECTION
    else:
        if position_open(user,symbol,product):
            if quantity > pos_quantity:
                amount = price * (quantity-pos_quantity)
                if wallet_checked(user,amount/2,product):
                    order = Order.objects.create(user=user,symbol=symbol,segment=segment,price=price,amount=total_amount,quantity=quantity,order_type=order_type,product=product,status="pending",type=type,charges=charges,stoploss=stoploss,target=target)
                    thread = threading.Thread(target=place_limit_order, args=(order.order_id,stoploss,target))
                    thread.start()
                else:
                    order = Order.objects.create(user=user,symbol=symbol,segment=segment,price=price,amount=amount,quantity=(quantity-pos_quantity),order_type=order_type,product=product,status="failed",type=type,charges=0,message='Insufficient Funds',stoploss=stoploss,target=target)
                    return 'failed'
            if quantity < pos_quantity:
                order = Order.objects.create(user=user,symbol=symbol,segment=segment,price=price,amount=total_amount,quantity=quantity,order_type=order_type,product=product,status="pending",type=type,charges=charges,stoploss=stoploss,target=target)
                thread = threading.Thread(target=place_limit_order, args=(order.order_id,stoploss,target))
                thread.start()
            else:
                order = Order.objects.create(user=user,symbol=symbol,segment=segment,price=price,amount=total_amount,quantity=quantity,order_type=order_type,product=product,status="pending",type=type,charges=charges,stoploss=stoploss,target=target)
                thread = threading.Thread(target=place_limit_order, args=(order.order_id,stoploss,target))
                thread.start()
        else:
            if wallet_checked(user,total_amount/2,product):
                order = Order.objects.create(user=user,symbol=symbol,segment=segment,price=price,amount=total_amount,quantity=quantity,order_type=order_type,product=product,status="pending",type=type,charges=charges,stoploss=stoploss,target=target)
                thread = threading.Thread(target=place_limit_order, args=(order.order_id,stoploss,target))
                thread.start()
            else:
                order = Order.objects.create(user=user,symbol=symbol,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="failed",type=type,charges=0,message='Insufficient Funds',stoploss=stoploss,target=target)
                return 'failed'


# def limit_order(user,symbol,quantity,order_type,product,type='LIMIT'):
#     data = symbollist.get(symbol)
#     segment = data['segment']
#     amount = 0
#     price = get_price(symbol)
#     total_amount = price * quantity
#     charges = calc_carrage(total_amount,order_type,product)
#     order = Order.objects.create(user=user,symbol=symbol,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="initiated",type=type,charges=charges,stoploss=stoploss,target=target)
#     order.save()