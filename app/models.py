from django.db import models
from django.contrib.auth.models import AbstractUser
from app.manager import *
import random
import string
from django.utils import timezone
from wallet.calculation import add_amount, deduct_amount, calc_carrage, add_wallet, deduct_wallet
from django.db import models, transaction, IntegrityError
from app.symbols.getsymbols import get_instrument_key
import datetime
from app.orders.ShoonyaApipy.tests.test_place_order import shoonya_order

def generate_unique_id():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(10))


class Remarks(models.Model):
    remark = models.CharField(max_length=200)
    def __str__(self):
        return self.remark


order_type = [
        ('BUY', 'BUY'),
        ('SELL', 'SELL'),
    ]

producttype = [
        ('Intraday', 'Intraday'),
        ('Carryforward', 'Carryforward'),
    ]

types = [
        ('Market', 'Market'),
        ('Limit', 'Limit'),
    ]

order_status = [
        ('initiated', 'initiated'),
        ('pending', 'pending'),
        ('completed', 'completed'),
        ('cancelled', 'cancelled'),
        ('failed', 'failed'),
    ]

transaction_status = [
        ('REQUESTED', 'REQUESTED'),
        ('CANCELLED', 'CANCELLED'),
        ('COMPLETED', 'COMPLETED'),
    ]

t_type = [
        ('WITHDRAW', 'WITHDRAW'),
        ('DEPOSIT', 'DEPOSIT'),
    ]


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=12)
    verification_code = models.CharField(max_length=420,null=True,blank=True,default="")
    wallet = models.FloatField(default=0.0)
    margin = models.PositiveIntegerField(default=100)
    margin_used = models.FloatField(default=0.0)
    pan_number = models.CharField(max_length=50,default="", null=True,blank=True)
    bank_account_name = models.CharField(max_length=150,default="")
    bank_account_number = models.CharField(max_length=150,default="")
    upi_id = models.CharField(max_length=150,default="")
    ifsc_code = models.CharField(max_length=12,default="")
    api_orders = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']
    def save(self, *args, **kwargs):
        self.wallet = round(self.wallet, 2)
        self.margin_used = round(self.margin_used, 2)
        first = False
        if not self.pk:
            first = True
        super().save(*args, **kwargs)
        if first:
        # Create default watchlist entries for the new user
            default_watchlists = Watchlist.objects.filter(is_default=True)
            for watchlist in default_watchlists:
                Watchlist.objects.create(
                    user=self,
                    symbol=watchlist.symbol,
                    segment=watchlist.segment,
                    instrument_key=watchlist.instrument_key,
                    tag=watchlist.tag,
                    is_default=False
                )




class symbols(models.Model):
    symbol=models.CharField(max_length=150,default="")
    name=models.CharField(max_length=150,default="",null=True,blank=True)
    segment=models.CharField(max_length=150,default="")
    instrument_key=models.CharField(max_length=150,default="")
    ltp=models.FloatField(default=0)
    open=models.FloatField(default=0)
    close=models.FloatField(default=0)
    high=models.FloatField(default=0)
    low=models.FloatField(default=0)
    last_day_close=models.FloatField(default=0)
    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        unique_together = ['symbol','segment']

    def save(self, *args, **kwargs):
        # Ensure ltp is rounded to two decimal places
        self.ltp = round(self.ltp, 2)
        # Forcefully add two decimal digits if missing
        self.ltp = float(f"{self.ltp:.2f}")
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.symbol)    


class Instrument(models.Model):
    instrument_key = models.CharField(max_length=100)
    exchange_token = models.CharField(max_length=20, blank=True, null=True)
    tradingsymbol = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100)
    last_price = models.FloatField(blank=True, null=True)
    expiry = models.CharField(max_length=20, blank=True, null=True)
    strike = models.FloatField(blank=True, null=True)
    tick_size = models.FloatField(blank=True, null=True)
    lot_size = models.IntegerField(blank=True, null=True)
    instrument_type = models.CharField(max_length=20)
    option_type = models.CharField(max_length=20, blank=True, null=True)
    exchange = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Shoonya_Instrument(models.Model):
    exchange_token = models.CharField(max_length=10,null=True,blank=True)
    tradingsymbol = models.CharField(max_length=20, null=True,blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    exchange = models.CharField(max_length=10,null=True,blank=True)

    class Meta:
        verbose_name = "Shoonya Instrument"
        verbose_name_plural = "Shoonya Instruments"

    def __str__(self):
        return f"{self.tradingsymbol} ({self.exchange})"

class Shoonya_Orders(models.Model):
    datetime = models.DateTimeField(default=timezone.now,null=True)
    response = models.TextField(max_length=5000, null=True,blank=True)

    class Meta:
        verbose_name = "Shoonya Order"
        verbose_name_plural = "Shoonya Orders"

    def __str__(self):
        return f"{self.datetime} ({self.response})"

class tags(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    tag=models.CharField(max_length=50,default="")
    class Meta:
        verbose_name = "Watchlist tag"
        verbose_name_plural = "Watchlist tags"
        unique_together = ['user','tag']
    def __str__(self):
        return str(self.tag)


class Watchlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    symbol = models.CharField(max_length=150, default="")
    segment = models.CharField(max_length=150, default="")
    instrument_key = models.CharField(max_length=150, default="")
    lot_size = models.PositiveIntegerField(default=1,null=True,blank=True)
    tag = models.CharField(max_length=20, default="Favourites")
    is_default = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Watchlist"
        verbose_name_plural = "Watchlists"
        unique_together = ['user', 'symbol', 'segment']
    
    def save(self, *args, **kwargs):
        with transaction.atomic():
            try:
                instrument_key = get_instrument_key(self.symbol, self.segment)
                if instrument_key:
                    self.instrument_key = instrument_key
                    symbols_entry, created = symbols.objects.get_or_create(
                        symbol=self.symbol,
                        segment=self.segment,
                        defaults={'instrument_key': self.instrument_key}
                    )
                    if not created and symbols_entry.instrument_key != self.instrument_key:
                        symbols_entry.instrument_key = self.instrument_key
                        symbols_entry.save()
                    
                    self.lot_size = Instrument.objects.get(instrument_key=self.instrument_key).lot_size
                    super().save(*args, **kwargs)
            
            except IntegrityError:
                # Handle unique constraint violation
                # Example: update existing entry or notify user
                # For example:
                existing_watchlist = Watchlist.objects.get(symbol=self.symbol, segment=self.segment)
                # Update existing_watchlist or handle the error as per your application's logic

            except Exception as e:
                # Handle other exceptions
                print(f"Error saving Watchlist: {e}")



class Transaction(models.Model):
    transaction_id = models.CharField(max_length=10, unique=True, default=generate_unique_id, editable=False)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now,null=True)
    status = models.CharField(choices=transaction_status,max_length=15,default = "REQUESTED")
    transaction_type = models.CharField(choices=t_type,max_length=15,default = "WITHDRAW")
    amount = models.PositiveIntegerField(default=0.0)
    remark = models.ForeignKey(Remarks,on_delete=models.CASCADE,blank=True,null=True)
    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
    def save(self, *args, **kwargs):
        if self.status == 'REQUESTED':
            pass
        if self.status == 'CANCELLED':
            if self.transaction_type == 'WITHDRAW':
                add_wallet(self.user,self.amount)
        if self.status == 'COMPLETED':
            if self.transaction_type == 'DEPOSIT':
                add_wallet(self.user,self.amount)
            if self.transaction_type == 'WITHDRAW':
                deduct_wallet(self.user,self.amount)
        super().save(*args, **kwargs)
    def __str__(self):
      return self.transaction_id



class Position(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    position_id = models.CharField(max_length=10, unique=True, default=generate_unique_id, editable=False)
    quantity = models.IntegerField(default=0)
    last_traded_quantity = models.IntegerField(default=0)
    symbol = models.CharField(max_length=150, default="")
    instrument_key = models.CharField(max_length=150, default="")
    lot_size = models.PositiveIntegerField(default=1)
    segment=models.CharField(max_length=150,default="")
    token = models.PositiveIntegerField(default=0)
    product = models.CharField(choices=producttype,max_length=15,default = "Intraday")
    buy_price = models.FloatField(default=0.0)
    sell_price = models.FloatField(default=0.0)
    stoploss = models.FloatField(default=0.0)
    target = models.FloatField(default=0.0)
    created_at = models.DateTimeField(default=timezone.now)
    realised_pnl = models.FloatField(default=0.0)
    unrealised_pnl = models.FloatField(default=0.0)
    is_holding = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    security_amount = models.FloatField(default=0.0)
    last_traded_datetime = models.DateTimeField(default=timezone.now)
    def save(self, *args, **kwargs):
        # GETTING TOKEN
        self.last_traded_datetime = datetime.datetime.now()
        og = Instrument.objects.filter(instrument_key=self.instrument_key).first()
        self.symbol = og.tradingsymbol
        self.token = og.exchange_token
        self.segment = og.exchange
        self.lot_size = Instrument.objects.get(instrument_key=self.instrument_key).lot_size
        # TOKEN SAVED
        if self.last_traded_quantity < 0:
            self.last_traded_quantity = self.last_traded_quantity * -1
        self.buy_price = round(self.buy_price, 2)
        self.sell_price = round(self.sell_price, 2)
        # Calculate P&L when saving the model
        if self.quantity == 0:
            self.is_closed = True
            self.stoploss = 0
            self.target = 0
            self.unrealised_pnl = ((self.sell_price) - (self.buy_price)) * self.last_traded_quantity
            self.realised_pnl = round((self.realised_pnl + self.unrealised_pnl),2)
            self.unrealised_pnl = 0.0
            orders = Order.objects.filter(user=self.user,status='pending', type='Limit',position=self).iterator()
            for order in orders:
                order.delete()
        else:
            print('STOPLOSS CHECK')
            if int(self.stoploss) != 0 :
                from app.orders.limit import initiate_limit_order
                print('STOPLOSS')
                if self.quantity > 0:
                    print('EXIT')
                    initiate_limit_order(self.user,self.symbol,self.instrument_key,self.token,self.stoploss,abs(self.quantity),'SELL',self.product,0,0,slt='s')
                    print('BUY')
                else:
                    initiate_limit_order(self.user,self.symbol,self.instrument_key,self.token,self.stoploss,abs(self.quantity),'BUY',self.product,0,0,slt='s')
            if int(self.target) != 0:
                if self.quantity > 0:
                    initiate_limit_order(self.user,self.symbol,self.instrument_key,self.token,self.target,abs(self.quantity),'SELL',self.product,0,0,slt='t')
                else:
                    initiate_limit_order(self.user,self.symbol,self.instrument_key,self.token,self.target,abs(self.quantity),'BUY',self.product,0,0,slt='t')
            self.is_closed = False
        if self.product == 'Carryforward':
            self.is_holding = True
        super().save(*args, **kwargs)
    def __str__(self):
      return self.symbol

class Order(models.Model):
    order_id = models.CharField(max_length=10, unique=True, default=generate_unique_id, editable=False)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now,null=True)
    symbol = models.CharField(max_length=150,default="")
    instrument_key = models.CharField(max_length=150,default="",blank=True)
    segment = models.CharField(max_length=150,default="")
    status = models.CharField(max_length=10,choices=order_status,default="pending")
    price = models.FloatField(default=0.0)
    quantity = models.PositiveIntegerField(default=0)
    amount = models.FloatField(default=0.0)
    stoploss = models.FloatField(default=0.0)
    target = models.FloatField(default=0.0)
    order_type = models.CharField(choices=order_type,max_length=5,default="")
    product = models.CharField(choices=producttype,max_length=15,default = "Intraday")
    type = models.CharField(choices=types,max_length=7,default = "Market")
    charges = models.FloatField(default=0.0)
    message = models.CharField(max_length=200,default = "",blank=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE,null = True,blank=True)
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
    def save(self, *args, **kwargs):
        print('-==-=Debuging-==-=-')
        self.charges = round(calc_carrage(self.amount,self.order_type,self.product), 2)
        self.amount = round(self.amount, 2)
        self.price = round(float(self.price), 2)

        if self.status == 'initiated':
            deduct_amount(self.user,self.charges)
            self.status = 'pending'
        elif self.status == 'failed' or self.status == 'cancelled':
            if self.type == 'Market':
                add_amount(self.user,self.charges)
        # else:
            # if self.user.api_orders:
            #     try:
            #         print('shoonya order -=-=-=-=')
            #         price = shoonya_order(self)
            #         print(price)
            #         if self.type == 'Market':
            #             try:
            #                 if price:
            #                     self.price = price
            #                     super().save(*args, **kwargs)
            #             except:
            #                 pass
            #     except:
            #         pass
                    # alice_order(self.symbol,self.quantity,self.order_type,self.product)
        super().save(*args, **kwargs)

    def __str__(self):
      return self.symbol


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)  # Assuming a maximum of 15 characters for a phone number
    query = models.TextField()
    date_time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.last_name else self.first_name
    class Meta:
        verbose_name = "Contact Us Request"
        verbose_name_plural = "Contact Requests"

class OnstockBalanceHistory(models.Model):
    datefield = models.DateField(default=timezone.now)
    balance = models.FloatField(default=0.0)
    pnl = models.FloatField(default=0.0)
    brokerage = models.FloatField(default=0.0)
    def __str__(self):
        return f"{self.datefield} --> {self.balance}"
    
    def save(self, *args, **kwargs):
        # TOTAL BALANCE
        total_balance = 0
        for x in CustomUser.objects.all():
            total_balance = total_balance + x.wallet
        total_balance = "{:.2f}".format(total_balance)
        self.balance = total_balance
        # END TOTAL BALANCE
        # TOTAL PNL
        today = timezone.now().date()
        close_positions = Position.objects.filter(last_traded_datetime__date=today,is_closed=True)
        total_pnl = 0
        for x in close_positions:
            total_pnl = total_pnl + x.realised_pnl
        self.pnl = "{:.2f}".format(total_pnl)
        # TOTAL END PNL
        # TOTAL BROKERAGE
        brokerage_collected = 0
        orders = Order.objects.filter(datetime__date=today, status='completed').order_by('-datetime')
        for x in orders:
            brokerage_collected += x.charges
        brokerage_collected = "{:.2f}".format(brokerage_collected)
        self.brokerage = brokerage_collected
        # TOTAL END BROKERAGE
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Onstock Balance"
        verbose_name_plural = "Onstock Balance History"
        unique_together = ['datefield']