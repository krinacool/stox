from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'wallet', 'margin','margin_used' ,'phone_number', 'api_orders', 'is_active','is_staff')
    list_filter = ('api_orders','is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Payment Info', {'fields': ('wallet' ,'margin', 'margin_used', 'bank_account_name','bank_account_number' ,'ifsc_code','upi_id')}),
        ('Permissions', {'fields': ('api_orders', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions', 'verification_code')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'phone_number', 'verification_code' ,'wallet', 'margin'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('email',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        
        if db_field.name == 'margin':
            formfield.widget.attrs.update({
                'placeholder': 'x',  # Adding a placeholder
            })

        return formfield
# Register the CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(symbols)
class Symbols(admin.ModelAdmin):
    list_display = ('symbol','segment','ltp','high','low','open','close')
    list_filter = ('symbol','segment')
    search_fields = ['symbol','segment']


@admin.register(Instrument)
class Instrument(admin.ModelAdmin):
    list_display = ('tradingsymbol','name','last_price','exchange','expiry','strike','tick_size','lot_size','instrument_type','option_type','exchange')
    list_filter = ('exchange',)
    search_fields = ('tradingsymbol',)


@admin.register(Watchlist)
class Watchlist(admin.ModelAdmin):
    list_display = ('user', 'symbol','segment','tag')
    list_filter = ('user', 'symbol','segment')


@admin.register(Transaction)
class Transaction(admin.ModelAdmin):
    list_display = ('user', 'amount','status','transaction_type','datetime', 'transaction_id', 'remark')
    list_filter = ('datetime', 'status', 'transaction_type','remark','user')


@admin.register(Order)
class Order(admin.ModelAdmin):
    list_display = ('user', 'symbol','order_type_color','price','charges','type', 'quantity','product','status_color','datetime','order_id')
    list_filter = ('datetime','status','user', 'symbol','order_type','type','product')
    def status_color(self, obj):
        if obj.status == 'completed':
            return format_html(f'<span style="color: green;">{obj.status}</span>', obj.status)
        elif obj.status == 'failed':
            return format_html(f'<span style="color: red;">{obj.status}</span>', obj.status)
        else:
            return format_html(f'<span style="color: blue;">{obj.status}</span>', obj.status)
    def order_type_color(self, obj):
        if obj.order_type == 'BUY':
            return format_html(f'<span style="color: green;">{obj.order_type}</span>', obj.order_type)
        elif obj.order_type == 'SELL':
            return format_html(f'<span style="color: red;">{obj.order_type}</span>', obj.order_type)
        else:
            return format_html(f'<span style="color: blue;">{obj.order_type}</span>', obj.order_type)
        
    status_color.short_description = 'Status'
    order_type_color.short_description = 'Order Type'

@admin.register(Position)
class Position(admin.ModelAdmin):
    # list_display = ('user','symbol','product','pnl')
    list_filter = ('created_at','user','symbol','product')
    list_display = ('user', 'quantity', 'symbol', 'product', 'buy_price', 'sell_price', 'pnl_colored','created_at')
    # Define a custom method to display pnl with color
    def pnl_colored(self, obj):
        if obj.realised_pnl < 0:
            return format_html(f'<span style="color: red;">{obj.realised_pnl}</span>', obj.realised_pnl)
        elif obj.realised_pnl > 0:
            return format_html(f'<span style="color: green;">{obj.realised_pnl}</span>', obj.realised_pnl)
        else:
            return obj.realised_pnl

    pnl_colored.short_description = 'P&L'


@admin.register(Contact)
class Contact(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number','date_time')


# ----------Admin Customization------------
admin.site.site_header="Onstock"
admin.site.site_title="Trading on your way"
# admin.site.index_template="home.html"
admin.site.index_title="Onstock | Admin"
admin.site.unregister(Group)
