from django.db import models
# from smartapi import SmartConnect
from app.symbols.getsymbols import get_symbol
import pyotp
from django.core.cache import cache
from app.symbols.api_sessions import sessions

class charges(models.Model):
    tax=models.FloatField(default=0.5)
    intraday_buy_charge=models.PositiveIntegerField(default=0)
    intraday_sell_charge=models.PositiveIntegerField(default=0)
    carryforward_buy_charge=models.PositiveIntegerField(default=0)
    carryforward_sell_charge=models.PositiveIntegerField(default=0)
    order_closing_charge=models.PositiveIntegerField(default=0)
    class Meta:
        verbose_name = "Charges"
        verbose_name_plural = "Charges"
    def __str__(self):
      return "Updated"

class Api(models.Model):
    user_id = models.CharField(max_length=120,default="")
    api_key = models.CharField(max_length=555,default="")
    class Meta:
        verbose_name = "Api Settings"
        verbose_name_plural = "Api Settings"
    def __str__(self):
      return self.user_id


class dates(models.Model):
    date = models.IntegerField()
    def __str__(self):
        return f"{self.date}"

class nse_market_time(models.Model):
    open_time = models.TimeField()
    close_time = models.TimeField()
    market_dates = models.ManyToManyField(dates,blank=True)
    class Meta:
        verbose_name = "NSE Market Setting"
        verbose_name_plural = "NSE Market Settings"
    def __str__(self):
        return f"NSE Market ({self.open_time} - {self.close_time})"
    

class mcx_market_time(models.Model):
    open_time = models.TimeField()
    close_time = models.TimeField()
    market_dates = models.ManyToManyField(dates,blank=True)
    class Meta:
        verbose_name = "MCX Market Setting"
        verbose_name_plural = "MCX Market Settings"
    def __str__(self):
        return f"MCX Market ({self.open_time} - {self.close_time})"    
    


class AngelApi(models.Model):
    id=models.AutoField(primary_key=True)
    api_key = models.CharField(max_length=100)
    client_id = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    # Add other fields as needed
    class Meta:
        verbose_name = "Angel One API"
        verbose_name_plural = "Market API"

    # Method to establish a session
    def create_session(self):
        smartApi = SmartConnect(self.api_key)
        totp = pyotp.TOTP(self.token).now()
        smartApi.generateSession(self.client_id, self.password, totp)
        data=smartApi.ltpData('NSE','SBIN','3045')
        if data['message'] == 'Invalid Token':
            return False
        return smartApi
    
    def save(self, *args, **kwargs):
        try:
            ses = self.create_session()
            if ses is not False:
                cache.set(f'smartapi{self.id}', ses,timeout=24*60*60)
                sessions.append(ses)
                super(AngelApi, self).save(*args, **kwargs)
        except:
            pass
    def __str__(self):
        return self.api_key
    

class ShoonyaApi(models.Model):
    user = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    token = models.CharField(max_length=200)
    vendor_code = models.CharField(max_length=100)
    api_key = models.CharField(max_length=300)
    class Meta:
        verbose_name = "Shoonya API"
        verbose_name_plural = "Shoonya API"
    def __str__(self):
        return self.user    
    


class Upstox(models.Model):
    client_id = models.CharField(max_length=100, default='')
    redirect_uri = models.CharField(max_length=120, default='https://onstock.in/upstox_cred')
    api_key = models.CharField(max_length=1000)
    secret_key = models.CharField(max_length=300)
    code = models.CharField(max_length=100, default='Leave it blank')
    access_token = models.CharField(max_length=1000, default='Leave it blank')
    class Meta:
        verbose_name = "Upstox"
        verbose_name_plural = "Upstox API"
    def __str__(self):
        return self.client_id


class UpstoxAccessTokens(models.Model):
    access_token = models.CharField(max_length=1000, default='access token')
    class Meta:
        verbose_name = "Upstox Access Token"
        verbose_name_plural = "Upstox Access Tokens"

    def __str__(self):
        return self.access_token

class Option_Lot_Size(models.Model):
    symbol = models.CharField(max_length=50)
    segment = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=1)
    class Meta:
        verbose_name = "Options Lot Size"
        verbose_name_plural = "Options Lot sizes"
    def save(self, *args, **kwargs):
        self.symbol = get_symbol(self.symbol)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.symbol