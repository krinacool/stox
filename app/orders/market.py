from app.symbols.details import get_price
from app.symbols.instruments import get_exchange
from wallet.calculation import wallet_checked ,deduct_amount, add_amount
from app.orders.position_logic import *
import time
from app.orders.ShoonyaApipy.tests.test_place_order import shoonya_order


# Market ORDER FUNCTION
def market_order(user,symbol,instrument_key,token,quantity,order_type,product,stoploss,target,type='MARKET'):
    from app.models import Order,symbols
    og = symbols.objects.filter(instrument_key=instrument_key).first()
    segment = og.segment
    amount = 0
    price = og.ltp
    pos = get_position(user,instrument_key,product)
    pos_quantity = 0
    if pos is not None:
        pos_quantity = pos.quantity
    if order_type == 'BUY':
        if scalp_position_open(user,instrument_key,product):
            pos_quantity = pos_quantity * -1
            if quantity > pos_quantity:
                # FIRST CLOSING POSITION
                # API USER
                if user.api_orders:
                    try:
                        print('shoonya order -=-=-=-=')
                        shoonyaPrice = shoonya_order(order_type,product,segment,instrument_key,quantity)
                        
                        if type == 'Market':
                            try:
                                if shoonyaPrice:
                                    try:
                                        if float(shoonyaPrice) < 25 and float(shoonyaPrice) > 5:
                                            shoonyaPrice = float(shoonyaPrice) + 0.5
                                        elif float(shoonyaPrice) < 50 and float(shoonyaPrice) > 25:
                                            shoonyaPrice = float(shoonyaPrice) + 0.75
                                        elif float(shoonyaPrice) < 100 and float(shoonyaPrice) > 50:
                                            shoonyaPrice = float(shoonyaPrice) + 1
                                        elif float(shoonyaPrice) < 200 and float(shoonyaPrice) > 100:
                                            shoonyaPrice = float(shoonyaPrice) + 1.5
                                        elif float(shoonyaPrice) < 400 and float(shoonyaPrice) > 200:
                                            shoonyaPrice = float(shoonyaPrice) + 2
                                        elif float(shoonyaPrice) > 400:
                                            shoonyaPrice = float(shoonyaPrice) + 3
                                    except:
                                        pass
                                    price = float(shoonyaPrice)
                            except:
                                pass
                    except:
                        pass
                # END API USER
                amount = pos_quantity * price
                order = Order.objects.create(user=user,symbol=symbol,instrument_key=instrument_key,segment=segment,price=price,amount=amount,quantity=pos_quantity,order_type=order_type,product=product,status="initiated",type=type,stoploss=0,target=0)
                order.status = 'completed'
                order.save()
                close_full_position(user,instrument_key,product,price)
                # CREATING NEW POSIITION
                quantity = quantity-pos_quantity
                amount = price * quantity
                if wallet_checked(user,amount,product):
                        # API USER
                    if user.api_orders:
                        try:
                            print('shoonya order -=-=-=-=')
                            shoonyaPrice = shoonya_order(order_type,product,segment,instrument_key,quantity)
                            
                            if type == 'Market':
                                try:
                                    if shoonyaPrice:
                                        try:
                                            if float(shoonyaPrice) < 25 and float(shoonyaPrice) > 5:
                                                shoonyaPrice = float(shoonyaPrice) + 0.5
                                            elif float(shoonyaPrice) < 50 and float(shoonyaPrice) > 25:
                                                shoonyaPrice = float(shoonyaPrice) + 0.75
                                            elif float(shoonyaPrice) < 100 and float(shoonyaPrice) > 50:
                                                shoonyaPrice = float(shoonyaPrice) + 1
                                            elif float(shoonyaPrice) < 200 and float(shoonyaPrice) > 100:
                                                shoonyaPrice = float(shoonyaPrice) + 1.5
                                            elif float(shoonyaPrice) < 400 and float(shoonyaPrice) > 200:
                                                shoonyaPrice = float(shoonyaPrice) + 2
                                            elif float(shoonyaPrice) > 400:
                                                shoonyaPrice = float(shoonyaPrice) + 3
                                        except:
                                            pass
                                        price = float(shoonyaPrice)
                                except:
                                    pass
                        except:
                            pass
                    # END API USER
                    amount = price * quantity
                    order = Order.objects.create(user=user,symbol=symbol,instrument_key=instrument_key,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="completed",type=type,stoploss=stoploss,target=target)
                    createPosition(user,instrument_key,quantity,order_type,product,price,stoploss,target)
                    deduct_amount(user,amount)
                else:
                    order = Order.objects.create(user=user,symbol=symbol,instrument_key=instrument_key,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="initiated",type=type,message='Insufficient Funds',stoploss=stoploss,target=target)
                    order.status = 'failed'
                    order.save()
                    return 'failed'
            elif quantity < pos_quantity:
                # API USER
                if user.api_orders:
                    try:
                        print('shoonya order -=-=-=-=')
                        shoonyaPrice = shoonya_order(order_type,product,segment,instrument_key,quantity)
                        
                        if type == 'Market':
                            try:
                                if shoonyaPrice:
                                    try:
                                        if float(shoonyaPrice) < 25 and float(shoonyaPrice) > 5:
                                            shoonyaPrice = float(shoonyaPrice) + 0.5
                                        elif float(shoonyaPrice) < 50 and float(shoonyaPrice) > 25:
                                            shoonyaPrice = float(shoonyaPrice) + 0.75
                                        elif float(shoonyaPrice) < 100 and float(shoonyaPrice) > 50:
                                            shoonyaPrice = float(shoonyaPrice) + 1
                                        elif float(shoonyaPrice) < 200 and float(shoonyaPrice) > 100:
                                            shoonyaPrice = float(shoonyaPrice) + 1.5
                                        elif float(shoonyaPrice) < 400 and float(shoonyaPrice) > 200:
                                            shoonyaPrice = float(shoonyaPrice) + 2
                                        elif float(shoonyaPrice) > 400:
                                            shoonyaPrice = float(shoonyaPrice) + 3
                                    except:
                                        pass
                                    price = float(shoonyaPrice)
                            except:
                                pass
                    except:
                        pass
                # END API USER
                amount = quantity * price
                order = Order.objects.create(user=user,symbol=symbol,instrument_key=instrument_key,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="initiated",type=type,stoploss=0,target=0)
                order.status = 'completed'
                order.save()
                close_some_position(user,instrument_key,quantity,product,price)
            else:
                                # API USER
                if user.api_orders:
                    try:
                        print('shoonya order -=-=-=-=')
                        shoonyaPrice = shoonya_order(order_type,product,segment,instrument_key,quantity)
                        
                        if type == 'Market':
                            try:
                                if shoonyaPrice:
                                    try:
                                        if float(shoonyaPrice) < 25 and float(shoonyaPrice) > 5:
                                            shoonyaPrice = float(shoonyaPrice) + 0.5
                                        elif float(shoonyaPrice) < 50 and float(shoonyaPrice) > 25:
                                            shoonyaPrice = float(shoonyaPrice) + 0.75
                                        elif float(shoonyaPrice) < 100 and float(shoonyaPrice) > 50:
                                            shoonyaPrice = float(shoonyaPrice) + 1
                                        elif float(shoonyaPrice) < 200 and float(shoonyaPrice) > 100:
                                            shoonyaPrice = float(shoonyaPrice) + 1.5
                                        elif float(shoonyaPrice) < 400 and float(shoonyaPrice) > 200:
                                            shoonyaPrice = float(shoonyaPrice) + 2
                                        elif float(shoonyaPrice) > 400:
                                            shoonyaPrice = float(shoonyaPrice) + 3
                                    except:
                                        pass
                                    price = float(shoonyaPrice)
                            except:
                                pass
                    except:
                        pass
                # END API USER
                amount = quantity * price
                order = Order.objects.create(user=user,symbol=symbol,instrument_key=instrument_key,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="initiated",type=type,stoploss=0,target=0)
                order.status = 'completed'
                order.save()
                close_full_position(user,instrument_key,product,price)
        # SCALP POSITION IS NOT OPEN
        else:
            amount = float(quantity) * price
            if wallet_checked(user,amount,product):
                                # API USER
                if user.api_orders:
                    try:
                        print('shoonya order -=-=-=-=')
                        shoonyaPrice = shoonya_order(order_type,product,segment,instrument_key,quantity)
                        
                        if type == 'Market':
                            try:
                                if shoonyaPrice:
                                    try:
                                        if float(shoonyaPrice) < 25 and float(shoonyaPrice) > 5:
                                            shoonyaPrice = float(shoonyaPrice) + 0.5
                                        elif float(shoonyaPrice) < 50 and float(shoonyaPrice) > 25:
                                            shoonyaPrice = float(shoonyaPrice) + 0.75
                                        elif float(shoonyaPrice) < 100 and float(shoonyaPrice) > 50:
                                            shoonyaPrice = float(shoonyaPrice) + 1
                                        elif float(shoonyaPrice) < 200 and float(shoonyaPrice) > 100:
                                            shoonyaPrice = float(shoonyaPrice) + 1.5
                                        elif float(shoonyaPrice) < 400 and float(shoonyaPrice) > 200:
                                            shoonyaPrice = float(shoonyaPrice) + 2
                                        elif float(shoonyaPrice) > 400:
                                            shoonyaPrice = float(shoonyaPrice) + 3
                                    except:
                                        pass
                                    price = float(shoonyaPrice)
                            except:
                                pass
                    except:
                        pass
                # END API USER
                amount = float(quantity) * price
                order = Order.objects.create(user=user,symbol=symbol,instrument_key=instrument_key,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="initiated",type=type,stoploss=stoploss,target=target)
                order.status = 'completed'
                order.save()
                deduct_amount(user,amount)
                # POSITION SETTLEMENT
                if get_position(user,instrument_key,product) is not None:
                    if position_open(user,instrument_key,product):
                        print('this 3')
                        add_more_position(user,instrument_key,quantity,product,price,stoploss,target)
                    else:
                        print('this 2')
                        createPosition(user,instrument_key,quantity,order_type,product,price,stoploss,target)
                else:
                    print('this 1')
                    createPosition(user,instrument_key,quantity,order_type,product,price,stoploss,target)
                # END POSITION SETTLEMENT
            else:
                print('Wallet failed')
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
                                                    # API USER
                    if user.api_orders:
                        try:
                            print('shoonya order -=-=-=-=')
                            shoonyaPrice = shoonya_order(order_type,product,segment,instrument_key,quantity)
                            
                            if type == 'Market':
                                try:
                                    if shoonyaPrice:
                                        try:
                                            if float(shoonyaPrice) < 25 and float(shoonyaPrice) > 5:
                                                shoonyaPrice = float(shoonyaPrice) + 0.5
                                            elif float(shoonyaPrice) < 50 and float(shoonyaPrice) > 25:
                                                shoonyaPrice = float(shoonyaPrice) + 0.75
                                            elif float(shoonyaPrice) < 100 and float(shoonyaPrice) > 50:
                                                shoonyaPrice = float(shoonyaPrice) + 1
                                            elif float(shoonyaPrice) < 200 and float(shoonyaPrice) > 100:
                                                shoonyaPrice = float(shoonyaPrice) + 1.5
                                            elif float(shoonyaPrice) < 400 and float(shoonyaPrice) > 200:
                                                shoonyaPrice = float(shoonyaPrice) + 2
                                            elif float(shoonyaPrice) > 400:
                                                shoonyaPrice = float(shoonyaPrice) + 3
                                        except:
                                            pass
                                        price = float(shoonyaPrice)
                                except:
                                    pass
                        except:
                            pass
                    # END API USER
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
                                                # API USER
                if user.api_orders:
                    try:
                        print('shoonya order -=-=-=-=')
                        shoonyaPrice = shoonya_order(order_type,product,segment,instrument_key,quantity)
                        
                        if type == 'Market':
                            try:
                                if shoonyaPrice:
                                    try:
                                        if float(shoonyaPrice) < 25 and float(shoonyaPrice) > 5:
                                            shoonyaPrice = float(shoonyaPrice) + 0.5
                                        elif float(shoonyaPrice) < 50 and float(shoonyaPrice) > 25:
                                            shoonyaPrice = float(shoonyaPrice) + 0.75
                                        elif float(shoonyaPrice) < 100 and float(shoonyaPrice) > 50:
                                            shoonyaPrice = float(shoonyaPrice) + 1
                                        elif float(shoonyaPrice) < 200 and float(shoonyaPrice) > 100:
                                            shoonyaPrice = float(shoonyaPrice) + 1.5
                                        elif float(shoonyaPrice) < 400 and float(shoonyaPrice) > 200:
                                            shoonyaPrice = float(shoonyaPrice) + 2
                                        elif float(shoonyaPrice) > 400:
                                            shoonyaPrice = float(shoonyaPrice) + 3
                                    except:
                                        pass
                                    price = float(shoonyaPrice)
                            except:
                                pass
                    except:
                        pass
                # END API USER
                amount = float(quantity) * price
                order = Order.objects.create(user=user,symbol=symbol,instrument_key=instrument_key,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="initiated",type=type,stoploss=stoploss,target=target)
                order.save()
                order.status = 'completed'
                order.save()
                close_some_position(user,instrument_key,quantity,product,price)
                add_amount(user,amount)
            else:
                                                # API USER
                if user.api_orders:
                    try:
                        print('shoonya order -=-=-=-=')
                        shoonyaPrice = shoonya_order(order_type,product,segment,instrument_key,quantity)
                        
                        if type == 'Market':
                            try:
                                if shoonyaPrice:
                                    try:
                                        if float(shoonyaPrice) < 25 and float(shoonyaPrice) > 5:
                                            shoonyaPrice = float(shoonyaPrice) + 0.5
                                        elif float(shoonyaPrice) < 50 and float(shoonyaPrice) > 25:
                                            shoonyaPrice = float(shoonyaPrice) + 0.75
                                        elif float(shoonyaPrice) < 100 and float(shoonyaPrice) > 50:
                                            shoonyaPrice = float(shoonyaPrice) + 1
                                        elif float(shoonyaPrice) < 200 and float(shoonyaPrice) > 100:
                                            shoonyaPrice = float(shoonyaPrice) + 1.5
                                        elif float(shoonyaPrice) < 400 and float(shoonyaPrice) > 200:
                                            shoonyaPrice = float(shoonyaPrice) + 2
                                        elif float(shoonyaPrice) > 400:
                                            shoonyaPrice = float(shoonyaPrice) + 3
                                    except:
                                        pass
                                    price = float(shoonyaPrice)
                            except:
                                pass
                    except:
                        pass
                # END API USER
                amount = quantity * price
                order = Order.objects.create(user=user,symbol=symbol,instrument_key=instrument_key,segment=segment,price=price,amount=amount,quantity=quantity,order_type=order_type,product=product,status="initiated",type=type,stoploss=0,target=0)
                order.status = 'completed'
                order.save()
                close_full_position(user,instrument_key,product,price)
                add_amount(user,amount)
        else:
            from app.models import Instrument
            instr = Instrument.objects.filter(instrument_key=instrument_key).first()
            if instr.option_type:
                if instr.option_type.upper() == 'CE' or instr.option_type.upper() == 'PE':
                    return 'failed'
            amount = price * quantity
            if wallet_checked(user,amount/2,product):
                # API USER
                if user.api_orders:
                    try:
                        print('shoonya order -=-=-=-=')
                        shoonyaPrice = shoonya_order(order_type,product,segment,instrument_key,quantity)
                        
                        if type == 'Market':
                            try:
                                if shoonyaPrice:
                                    try:
                                        if float(shoonyaPrice) < 25 and float(shoonyaPrice) > 5:
                                            shoonyaPrice = float(shoonyaPrice) + 0.5
                                        elif float(shoonyaPrice) < 50 and float(shoonyaPrice) > 25:
                                            shoonyaPrice = float(shoonyaPrice) + 0.75
                                        elif float(shoonyaPrice) < 100 and float(shoonyaPrice) > 50:
                                            shoonyaPrice = float(shoonyaPrice) + 1
                                        elif float(shoonyaPrice) < 200 and float(shoonyaPrice) > 100:
                                            shoonyaPrice = float(shoonyaPrice) + 1.5
                                        elif float(shoonyaPrice) < 400 and float(shoonyaPrice) > 200:
                                            shoonyaPrice = float(shoonyaPrice) + 2
                                        elif float(shoonyaPrice) > 400:
                                            shoonyaPrice = float(shoonyaPrice) + 3
                                    except:
                                        pass
                                    price = float(shoonyaPrice)
                            except:
                                pass
                    except:
                        pass
                # END API USER
                amount = float(quantity) * price
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
