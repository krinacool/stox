from django.db import models
import pyotp
import datetime
from django.core.cache import cache
from app.symbols.api_sessions import sessions

class charges(models.Model):
    tax=models.FloatField(default=0.5)
    order_closing_charge=models.PositiveIntegerField(default=0)

    manipulate_5_to_25 = models.FloatField(default=0.25)
    manipulate_25_to_50 = models.FloatField(default=0.45)
    manipulate_50_to_100 = models.FloatField(default=0.65)
    manipulate_100_to_200 = models.FloatField(default=1.25)
    manipulate_200_to_400 = models.FloatField(default=1.45)
    manipulate_400_or_above = models.FloatField(default=2.25)
    
    class Meta:
        verbose_name = "Charges"
        verbose_name_plural = "Charges"
    def __str__(self):
      return "Updated"

class dates(models.Model):
    date = models.IntegerField()
    def __str__(self):
        return f"{self.date}"

class nse_market_time(models.Model):
    open_time = models.TimeField()
    close_time = models.TimeField()
    position_close_time = models.TimeField(default=datetime.time(15, 20))  # 3:20 PM
    market_dates = models.ManyToManyField(dates,blank=True)
    class Meta:
        verbose_name = "NSE Market Setting"
        verbose_name_plural = "NSE Market Settings"
    def __str__(self):
        return f"NSE Market ({self.open_time} - {self.close_time})"
    

class mcx_market_time(models.Model):
    open_time = models.TimeField()
    close_time = models.TimeField()
    position_close_time = models.TimeField(default=datetime.time(23, 20))  # 3:20 PM
    market_dates = models.ManyToManyField(dates,blank=True)
    class Meta:
        verbose_name = "MCX Market Setting"
        verbose_name_plural = "MCX Market Settings"
    def __str__(self):
        return f"MCX Market ({self.open_time} - {self.close_time})"    
    

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


class PaymentGateway(models.Model):
    upi_id = models.CharField(max_length=500,default="")
    upi_token = models.CharField(max_length=500,default="")
    key = models.CharField(max_length=500,default="")
    
    payu_marchent_key = models.CharField(max_length=500,default="")
    payu_marchent_salt = models.CharField(max_length=500,default="")
    class Meta:
        verbose_name = "Payment Gateway Setting"
        verbose_name_plural = "Payment Gateway"
    def __str__(self):
      return "Payment Gateway"