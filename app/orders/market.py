from app.symbols.details import get_price
from app.symbols.instruments import get_exchange
from wallet.calculation import wallet_checked ,deduct_amount, add_amount
from app.orders.position_logic import *
import time


# Market ORDER FUNCTION
def market_order(user,symbol,instrument_key,token,quantity,order_type,product,stoploss,target,type='MARKET'):
    from app.models import Order
    segment = get_exchange(token)
    amount = 0
    price = get_price(instrument_key)
    pos = get_position(user,instrument_key,product)
    pos_quantity = 0
    if pos is not None:
        pos_quantity = pos.quantity
    if order_type == 'BUY':
        if scalp_position_open(user,instrument_key,product):
            pos_quantity = pos_quantity * -1
            if quantity > pos_quantity:
                # FIRST CLOSING POSITION
                amount = pos_quantity * price
                order = Order.objects.create(user=user,symbol=symbol,instrument_key=instrument_key,segment=segment,price=price,amount=amount,quantity=pos_quantity,order_type=order_type,product=product,status="initiated",type=type,stoploss=0,target=0)
                order.status = 'completed'
                order.save()
                close_full_position(user,instrument_key,product,price)
                # CREATING NEW POSIITION
                quantity = quantity-pos_quantity
                amount = price * quantity
                if wallet_checked(user,amount,product):
                    order = Order.objects.create(user=user,symbol=symbol,instrument_key=instrument_key,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="completed",type=type,stoploss=stoploss,target=target)
                    createPosition(user,instrument_key,quantity,order_type,product,price,stoploss,target)
                    deduct_amount(user,amount)
                else:
                    order = Order.objects.create(user=user,symbol=symbol,instrument_key=instrument_key,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="initiated",type=type,message='Insufficient Funds',stoploss=stoploss,target=target)
                    order.status = 'failed'
                    order.save()
                    return 'failed'
            elif quantity < pos_quantity:
                amount = quantity * price
                order = Order.objects.create(user=user,symbol=symbol,instrument_key=instrument_key,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="initiated",type=type,stoploss=0,target=0)
                order.status = 'completed'
                order.save()
                close_some_position(user,instrument_key,quantity,product,price)
            else:
                amount = quantity * price
                order = Order.objects.create(user=user,symbol=symbol,instrument_key=instrument_key,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="initiated",type=type,stoploss=0,target=0)
                order.status = 'completed'
                order.save()
                close_full_position(user,instrument_key,product,price)
        # SCALP POSITION IS NOT OPEN
        else:
            amount = quantity * price
            if wallet_checked(user,amount,product):
                order = Order.objects.create(user=user,symbol=symbol,instrument_key=instrument_key,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="initiated",type=type,stoploss=stoploss,target=target)
                order.status = 'completed'
                order.save()
                deduct_amount(user,amount)
                # POSITION SETTLEMENT
                if get_position(user,instrument_key,product) is not None:
                    if position_open(user,instrument_key,product):
                        add_more_position(user,instrument_key,quantity,product,price,stoploss,target)
                    else:
                        createPosition(user,instrument_key,quantity,order_type,product,price,stoploss,target)
                else:
                    createPosition(user,instrument_key,quantity,order_type,product,price,stoploss,target)
                # END POSITION SETTLEMENT
            else:
                order = Order.objects.create(user=user,symbol=symbol,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="initiated",type=type,message='Insufficient Funds',stoploss=stoploss,target=target)
                order.status = 'failed'
                order.save()
                return 'failed'
    # SELL SECTION
    else:
        if position_open(user,instrument_key,product):
            if quantity > pos_quantity:
                amount = price * pos_quantity
                order = Order.objects.create(user=user,symbol=symbol,instrument_key=instrument_key,segment=segment,price=price,amount=amount,quantity=pos_quantity,order_type=order_type,product=product,status="initiated",type=type,stoploss=stoploss,target=target)
                order.status = 'completed'
                order.save()
                close_full_position(user,instrument_key,product,price)
                add_amount(user,amount)
                if wallet_checked(user,amount/2,product):
                    quantity = quantity - pos_quantity
                    amount = quantity * price
                    order = Order.objects.create(user=user,symbol=symbol,instrument_key=instrument_key,segment=segment,price=price,amount=amount,quantity=pos_quantity,order_type=order_type,product=product,status="initiated",type=type,stoploss=stoploss,target=target)
                    order.status = 'completed'
                    order.save()
                    createPosition(user,instrument_key,quantity,order_type,product,price,stoploss,target)
                    add_amount(user,(amount))
                else:
                    order = Order.objects.create(user=user,symbol=symbol,instrument_key=instrument_key,segment=segment,price=price,amount=amount,quantity=(quantity-pos_quantity),order_type=order_type,product=product,status="initiated",type=type,message='Insufficient Funds',stoploss=stoploss,target=target)
                    order.status = 'failed'
                    return 'failed'
            if quantity < pos_quantity:
                amount = quantity * price
                order = Order.objects.create(user=user,symbol=symbol,instrument_key=instrument_key,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="initiated",type=type,stoploss=stoploss,target=target)
                order.save()
                order.status = 'completed'
                order.save()
                close_some_position(user,instrument_key,quantity,product,price)
                add_amount(user,amount)
            else:
                amount = quantity * price
                order = Order.objects.create(user=user,symbol=symbol,instrument_key=instrument_key,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="initiated",type=type,stoploss=0,target=0)
                order.status = 'completed'
                order.save()
                close_full_position(user,instrument_key,product,price)
                add_amount(user,amount)
        else:
            amount = price * quantity
            if wallet_checked(user,amount/2,product):
                order = Order.objects.create(user=user,symbol=symbol,instrument_key=instrument_key,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="initiated",type=type,stoploss=stoploss,target=target)
                order.status = 'completed'
                order.save()
                deduct_amount(user,amount)
                if scalp_position_open(user,instrument_key,product):
                    add_more_position(user,instrument_key,quantity,product,price,stoploss,target)
                    add_amount(user,amount)
                else:
                    createPosition(user,instrument_key,quantity,order_type,product,price,stoploss,target)
                    add_amount(user,amount)
            else:
                order = Order.objects.create(user=user,symbol=symbol,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="initiated",type=type,message='Insufficient Funds',stoploss=stoploss,target=target)
                order.status = 'failed'
                order.save()
                return 'failed'





def stoploss_target(order_id):
    from app.models import Order
    order = Order.objects.get(order_id=order_id)
    stoploss = order.stoploss
    target = order.target
    start_time = time.time()
    current_price = get_price(order.symbol)
    # while time.time() - start_time < 50400:
    while True:
        order = Order.objects.get(order_id=order_id)
        try:
            if order.stoploss != stoploss or order.target != target:
                return 'failed'
            if order.quantity == '0':
                return 'failed'
            elif order.quantity > 1:
                if (order.stoploss >= current_price or current_price >= order.target):
                    market_order(order.user,order.symbol,order.quantity,'SELL',order.product,0,0,'MARKET')
                    return 'success'
            else:
                if (order.stoploss <= current_price or current_price <= order.target):
                    market_order(order.user,order.symbol,order.quantity,'BUY',order.product,0,0,'MARKET')
                    return 'success'
            current_price = get_price(order.symbol)
        except Exception as e:
            return 'failed'

                



    #         Order.objects.create(user=user,symbol=symbol,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="completed",type='Market',message='Order excuted successfully.')
    #         deduct_amount(user,amount)
    #         createPosition(user,symbol,quantity,order_type,product,price,stoploss,target,stoploss,target)
    #         if user.api_orders:
    #             try:
    #                 alice_order(symbol,quantity,order_type)
    #             except:
    #                 # HERE I CAN PUT ANOTHER API ORDER IF ABOVE FAILED
    #                 pass
    #         return "success"
    #     else:
    #         Order.objects.create(user=user,symbol=symbol,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="failed",type='Market',message='Insufficient Funds')
    #         return "failed"
    # else:
    #     amount = calc_carrage(total_amount,order_type)
    #     Order.objects.create(user=user,symbol=symbol,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="completed",type='Market',message='Order excuted successfully')
    #     createPosition(user,symbol,quantity,order_type,product,price,stoploss,target,stoploss,target)
    #     add_amount(user,amount)
    #     if user.api_orders:
    #         try:
    #             alice_order(symbol,quantity,order_type)
    #         except:
    #             pass
    #     return "success"
