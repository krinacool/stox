from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.db.models.functions import TruncDay
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.db.models import Sum


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'wallet', 'margin','margin_used' ,'phone_number', 'api_orders', 'is_active','is_staff')
    list_filter = ('api_orders','is_staff', 'is_active')
    readonly_fields = ('wallet','margin_used')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number','pan_number')}),
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


    def changelist_view(self, request, extra_context=None):
        # Aggregate new authors per day
        chart_data = (
            CustomUser.objects.annotate(date=TruncDay("date_joined"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )
        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        print("Json %s"%as_json)
        extra_context = extra_context or {"chart_data": as_json}
        # Call the superclass changelist_view to render the page

        return super().changelist_view(request, extra_context=extra_context)


    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        
        if db_field.name == 'margin':
            formfield.widget.attrs.update({
                'placeholder': 'x',  # Adding a placeholder
            })

        return formfield
# Register the CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Remarks)

@admin.register(symbols)
class Symbols(admin.ModelAdmin):
    list_display = ('symbol','segment','ltp','high','low','open','close','last_day_close')
    list_filter = ('symbol','segment')
    search_fields = ['symbol','segment']


@admin.register(Instrument)
class Instrument(admin.ModelAdmin):
    list_display = ('tradingsymbol','name','last_price','exchange','expiry','strike','tick_size','lot_size','instrument_type','option_type','exchange')
    list_filter = ('exchange',)
    search_fields = ('tradingsymbol',)

@admin.register(Shoonya_Instrument)
class Shoonya_Instrument(admin.ModelAdmin):
    list_display = ('exchange_token','tradingsymbol','name','exchange')
    list_filter = ('exchange',)
    search_fields = ('exchange_token','tradingsymbol','name','exchange')
    
@admin.register(Shoonya_Orders)
class ShoonyaOrderAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        # Aggregate new authors per day
        chart_data = (
            Transaction.objects.annotate(date=TruncDay("datetime"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )
        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        print("Json %s"%as_json)
        extra_context = extra_context or {"chart_data": as_json}
        # Call the superclass changelist_view to render the page

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(OnstockBalanceHistory)
class OnstockBalanceAdmin(admin.ModelAdmin):
    list_display = ('datefield','balance','pnl','brokerage','withdrawn','deposit')
    list_filter = ('datefield',)
    def changelist_view(self, request, extra_context=None):
        # Aggregate new authors per day
        chart_data = (
            OnstockBalanceHistory.objects.annotate(date=TruncDay("datefield"))
            .values("date")
            .annotate(y=Sum("balance"))  # Change 'Sum' based on your aggregation needs
            .order_by("-date")
        )
        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        print("Json %s"%as_json)
        extra_context = extra_context or {"chart_data": as_json}
        # Call the superclass changelist_view to render the page

        return super().changelist_view(request, extra_context=extra_context)



@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'symbol','segment','tag','is_default')
    list_filter = ('user', 'symbol','segment','is_default')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount','status','transaction_type', 'wallet','datetime', 'transaction_id', 'remark')
    list_filter = ('datetime', 'status', 'transaction_type','remark','user')
    readonly_fields = ('wallet',)
    
    def changelist_view(self, request, extra_context=None):
        # Aggregate new authors per day
        chart_data = (
            Transaction.objects.annotate(date=TruncDay("datetime"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )
        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        print("Json %s"%as_json)
        extra_context = extra_context or {"chart_data": as_json}
        # Call the superclass changelist_view to render the page

        return super().changelist_view(request, extra_context=extra_context)



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'symbol','order_type_color','price','charges','type', 'quantity','product','status_color','datetime','order_id')
    list_filter = ('datetime','status','user', 'symbol','order_type','type','product')

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        try:
            cl = self.get_changelist_instance(request)
            queryset = cl.get_queryset(request)
        except Exception as e:
            queryset = self.get_queryset(request)
        if hasattr(response, 'context_data'):
            response.context_data['filtered_queryset'] = queryset
        total_brokerage = 0
        for x in queryset:
            total_brokerage = total_brokerage + x.charges
        total_brokerage = "{:.2f}".format(total_brokerage)
        chart_data = (
            Order.objects.annotate(date=TruncDay("datetime"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}
        extra_context["total_brokerage"] = total_brokerage 

        return super().changelist_view(request, extra_context=extra_context)


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
class PositionAdmin(admin.ModelAdmin):
    list_filter = ('created_at','user','symbol','product','last_traded_datetime')
    list_display = ('user', 'quantity','last_traded_quantity', 'symbol', 'product', 'buy_price', 'sell_price', 'pnl_colored','created_at','last_traded_datetime' ,'close_positon')

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        try:
            cl = self.get_changelist_instance(request)
            queryset = cl.get_queryset(request)
        except Exception as e:
            queryset = self.get_queryset(request)

        total_pnl = 0
        for x in queryset:
            total_pnl = total_pnl + x.realised_pnl
        
        if hasattr(response, 'context_data'):
            response.context_data['filtered_queryset'] = queryset

        # Aggregate new authors per day
        chart_data = (
            Position.objects.annotate(date=TruncDay("last_traded_datetime"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )
        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        print("Json %s"%as_json)
        extra_context = extra_context or {"chart_data": as_json}
        extra_context["total_pnl"] = "{:.2f}".format(total_pnl) 
        # Call the superclass changelist_view to render the page

        return super().changelist_view(request, extra_context=extra_context)

    # Define a custom method to display pnl with color
    def pnl_colored(self, obj):
        if obj.realised_pnl < 0:
            return format_html(f'<span style="color: red;">{obj.realised_pnl}</span>', obj.realised_pnl)
        elif obj.realised_pnl > 0:
            return format_html(f'<span style="color: green;">{obj.realised_pnl}</span>', obj.realised_pnl)
        else:
            return format_html(f'<span style="color: blue;">{obj.realised_pnl}</span>', obj.realised_pnl)

    pnl_colored.short_description = 'P&L'
    def close_positon(self, obj):
        return format_html(f'''
                           <a href='/closepos/{obj.id}'><button type='button' class='btn btn-danger'">Close</button></a>
                        ''')

    close_positon.short_description = 'Close Position'



@admin.register(Contact)
class Contact(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number','date_time')


# ----------Admin Customization------------
admin.site.site_header="Onstock"
admin.site.site_title="Trading on your way"
# admin.site.index_template="home.html"
admin.site.index_title="Onstock | Admin"
