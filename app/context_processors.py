# app/context_processors.py

from django.utils import timezone
from django.db.models.functions import TruncDay
from django.db.models import Count
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.timezone import now, timedelta
from .models import CustomUser, Transaction, Order

def custom_admin_context(request):
    context = {}

    if request.path.startswith('/admin/'):
        total_balance = 0
        all_users = CustomUser.objects.all()
        today = timezone.now().date()
        transactions = Transaction.objects.filter(status='COMPLETED', datetime__date=today)
        brokerage_collected = 0
        orders = Order.objects.filter(user=request.user, datetime__date=today, status='completed').order_by('-datetime')

        for x in orders:
            brokerage_collected += x.charges

        total_deposit = 0
        total_withdraw = 0

        for x in transactions:
            if x.transaction_type == 'DEPOSIT':
                total_deposit += x.amount
            else:
                total_withdraw += x.amount

        for x in all_users:
            total_balance += x.wallet

        total_balance = "{:.2f}".format(total_balance)

        # CHARTS
        thirty_days_ago = now() - timedelta(days=60)

        # Query for CustomUser objects joined in the last 30 days
        chart_data = CustomUser.objects.filter(date_joined__gte=thirty_days_ago) \
            .annotate(date=TruncDay("date_joined")) \
            .values("date") \
            .annotate(y=Count("id")) \
            .order_by("-date")

        # Query for Order objects created in the last 30 days
        chart_data2 = Order.objects.filter(datetime__gte=thirty_days_ago) \
            .annotate(date=TruncDay("datetime")) \
            .values("date") \
            .annotate(y=Count("id")) \
            .order_by("-date")

        # Query for Transaction objects with datetime in the last 30 days
        chart_data3 = Transaction.objects.filter(datetime__gte=thirty_days_ago) \
            .annotate(date=TruncDay("datetime")) \
            .values("date") \
            .annotate(y=Count("id")) \
            .order_by("-date")

        # Serialize chart data to JSON
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        as_json2 = json.dumps(list(chart_data2), cls=DjangoJSONEncoder)
        as_json3 = json.dumps(list(chart_data3), cls=DjangoJSONEncoder)

        context = {
            "total_balance": total_balance,
            "total_deposit": total_deposit,
            "total_withdraw": total_withdraw,
            "brokerage_collected": brokerage_collected,
            "total_users": all_users.count(),
            "api_users": all_users.filter(api_orders=True).count(),
            "chart_data": as_json,
            "chart_data2": as_json2,
            "chart_data3": as_json3,
        }

    return context
