from django.contrib import admin
from .models import *
import urllib.parse
from django.shortcuts import redirect
from django.utils.html import format_html

# Register your models here.
class BasicSettingAdmin(admin.ModelAdmin):
    model = charges
    list_display = ('tax', 'intraday_buy_charge', 'intraday_sell_charge', 'carryforward_buy_charge', 'carryforward_sell_charge')
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'tax':
            formfield.widget.attrs.update({
                'placeholder': '%',  # Adding a placeholder
            })
            formfield.help_text = 'The given value will be in Percentage(%)'

        return formfield
# Register the basicAdmin
admin.site.register(charges, BasicSettingAdmin)

@admin.register(Api)
class Api(admin.ModelAdmin):
    list_display = ('user_id', 'api_key')

@admin.register(AngelApi)
class AngelApi(admin.ModelAdmin):
    list_display = ('api_key', 'token')



from django.contrib import admin
from django.shortcuts import redirect
from .models import Upstox
import urllib.parse
from django import forms

class UpstoxForm(forms.ModelForm):
    class Meta:
        model = Upstox
        fields = '__all__'

    class Media:
        js = ('admin/js/upstox_admin.js',)

class UpstoxAdmin(admin.ModelAdmin):
    form = UpstoxForm
    list_display = ('client_id', 'api_key')
    # readonly_fields = ('redirect_uri',)

    def response_change(self, request, obj):
        self.message_user(request, "Upstox API activated")
        return redirect(f'https://api-v2.upstox.com/login/authorization/dialog?response_type=code&client_id={obj.api_key}&redirect_uri={urllib.parse.quote(obj.redirect_uri)}')

admin.site.register(Upstox, UpstoxAdmin)



@admin.register(nse_market_time)
class nse_market(admin.ModelAdmin):
    list_display = ('open_time', 'close_time')


@admin.register(mcx_market_time)
class mcx_market(admin.ModelAdmin):
    list_display = ('open_time', 'close_time')

@admin.register(ShoonyaApi)
class ShoonyaApi(admin.ModelAdmin):
    list_display = ('user', 'password', 'token', 'vendor_code', 'api_key')

@admin.register(Option_Lot_Size)
class Option_Lot_Size(admin.ModelAdmin):
    search_fields = ('symbol', 'segment', 'quantity')
    list_display = ('symbol', 'segment', 'quantity')

admin.site.register(UpstoxAccessTokens)