from settings.models import charges


def calc_carrage(amount,order_type,product,user):
    settings = charges.objects.first()
    carrage = 0
    tax = (settings.tax/100)*amount
    print(tax)
    carrage = carrage+tax
    if order_type == 'BUY':
        if product == 'Intraday':
            carrage = carrage + user.intraday_buy_charge
        else:
            carrage = carrage + user.carryforward_buy_charge
    else:
        if product == 'Intraday':
            carrage = carrage + user.intraday_sell_charge
        else:
            carrage = carrage + user.carryforward_sell_charge
    print(carrage)
    return carrage

def scalp_wallet_checked(user,amount,product):
    if (amount/2) <= user.wallet:
        return True
    else:
        return False

def wallet_checked(user,amount,product):
    max = 0
    if product == 'Intraday':
        max = (user.wallet * user.margin)
    else:
        max = user.wallet
    if amount < max:
        return True
    else:
        return False

def add_amount(user,amount):
    if amount < user.margin_used:
        user.margin_used = user.margin_used - amount
        user.save()
    else:
        new_amount = amount - user.margin_used
        user.margin_used = 0
        user.wallet = user.wallet + new_amount
        user.save()
    # user.wallet = float(user.wallet) + amount
    # user.save()

def deduct_amount(user,amount):
    # NOT USING MARGIN
    if user.wallet > amount:
        user.wallet = user.wallet - amount
        user.save()
    # # USING MARGIN
    # elif user.wallet < amount:
    #     print(amount)
    #     margin = user.margin
    #     bywallet = amount - (amount/margin)
    #     user.wallet = user.wallet - bywallet
    #     new_amount = amount - bywallet
    #     user.margin_used = user.margin_used + new_amount
    #     user.save()
    # # NO NEED FOR THAT
    else:
        new_amount = amount - user.wallet
        user.wallet = 0
        user.margin_used = user.margin_used + new_amount
        user.save()
    

def add_wallet(user,amount):
    user.wallet = float(user.wallet) + amount
    user.save()

def deduct_wallet(user,amount):
    user.wallet = float(user.wallet) - amount
    user.save()