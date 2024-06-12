import json
from settings.models import *
from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from app.models import *
from app.forms import *
from django.contrib.auth.decorators import login_required
from stock.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
import random
import string
from threading import Thread
from django.utils import timezone
from settings.timing import market_open
from wallet.calculation import *
from app.orders.market import market_order
from app.orders.limit import initiate_limit_order
from app.symbols.getsymbols import get_symbol
from settings.models import Option_Lot_Size

User = get_user_model()

# -=--------=---=----------=--=------PAGES--=---=------=---
# CONTACT US
def contact(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        user = form.save()
        messages.success(request,'We will contact to you as soon as possible')
    return render(request,"contact.html")

# ABOUT
def about(request):
    return render(request,"about.html")

def disclaimer(request):
    return render(request,"disclaimer.html")

# POLICY
def privacypolicy(request):
    return render(request,"privacypolicy.html")

def refundpolicy(request):
    return render(request,"refundpolicy.html")
# END PAGES

# USER CREATION LOGIN AND SIGNUP
def generate_verification_code(length=60):
    characters = string.ascii_letters + string.digits
    attempts = 0
    while True:
        verification_code = ''.join(random.choice(characters) for _ in range(length))
        if not CustomUser.objects.filter(verification_code=verification_code).exists():
            return verification_code
        attempts += 1

def verify_user(request,code):
    try:
       client = User.objects.filter(verification_code = code).first()
       client.is_active = True
       client.save()
       messages.success(request,'Congratulations ! Your email has been successfully verified Please login to continue.')       
       return redirect('/login/')
    except:
        return redirect('/')

def index(request):
    return render(request,'home.html')

def handlelogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/market')
            else:
                messages.error(request, 'Invalid login credentials.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def handlesignup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            verification_code = generate_verification_code()
            user.verification_code = verification_code
            user.save()
            subject = "E-mail verification for onstock Sign Up"
            html_content = render_to_string('email_template.html', {'verification_code': verification_code})
            content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                subject,
                content ,
                EMAIL_HOST_USER ,
                [user.email]
            )
            email.attach_alternative(html_content,'text/html')
            email.send()
            content = "An verification link has been sent to your email. Plese verify to continue."
            return render(request,'message.html',{'content':content})
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})

def handlelogout(request):
    logout(request)
    messages.success(request,"Logged out Successfully")
    return redirect('/login/')


# ---------------DASHBOARD
@login_required
def market(request):
    wl_list = Watchlist.objects.all().filter(tag='#@DEFAULT')
    wl = []
    print('wl_list')
    for x in wl_list:
        print(x)
        wl.append(x.instrument_key)
    wallet = request.user.wallet
    margin = request.user.margin
    settings = charges.objects.first()
    charge = settings.intraday_buy_charge
    tax = settings.tax
    option_chain = {}
    lotob = Option_Lot_Size.objects.all()
    for x in lotob:
        option_chain[x.symbol] = x.quantity
    # ---------------CONTEXT-----------
    context = {
        'wl':wl,
        'wl_list':wl_list,
        'wallet':wallet,
        'margin':margin,
        'charges':charge,
        'tax':tax,
        'option_chain':json.dumps(option_chain),
    }
    return render(request,'market.html',context)


@login_required
def watchlist(request):
    if request.method == 'POST':
        try:
            symbols = request.POST.get("symbollist")
            tag = request.POST.get("tag")
            symbols_data = eval(symbols)
            for x in symbols_data:
                try:
                    Watchlist.objects.create(user=request.user,token=x['exchange_token'],tag=tag)
                except:
                    pass
            messages.success(request,'Watchlist Updated !')
        except:
            messages.error(request,'Oops! Something went wrong.')
    # form = WatchlistForm()
    watch_list = Watchlist.objects.filter(user=request.user)
    watchlist_list = []
    watchlist_symbollist = []
    for i in watch_list:
        watchlist_symbollist.append(i.instrument_key)
        if i.tag not in watchlist_list:
            watchlist_list.append(i.tag)
    settings = charges.objects.first()
    charge = settings.intraday_buy_charge
    tax = settings.tax
    option_chain = {}
    lotob = Option_Lot_Size.objects.all()
    for x in lotob:
        option_chain[x.symbol] = x.quantity
    # ---------------CONTEXT-----------
    context = {
        "charges":charge,
        "watchlist_list":watchlist_list,
        "watch_list":watch_list,
        "watchlist_symbollist":watchlist_symbollist,
        "tax":tax,
        "option_chain":json.dumps(option_chain),
    }
    return render(request,'watchlist.html',context)




@login_required
def delete_symbol(request,symbol):
    try:
        de = Watchlist.objects.filter(user=request.user,instrument_key=symbol).first()
        de.delete()
    except:
        pass
    messages.success(request,'Watchlist updated successfully !')
    return redirect('/watchlist')


# -----------------------ORDERS
@login_required
def orders(request):
    today = timezone.now().date()
    completed = Order.objects.filter(user=request.user, datetime__date=today,status = 'completed').order_by('-datetime')    
    pending = Order.objects.filter(user=request.user, datetime__date=today,status = 'pending').order_by('-datetime')
    initiated = Order.objects.filter(user=request.user, datetime__date=today,status__in=['pending', 'initiated']).order_by('-datetime')
    failed = Order.objects.filter(user=request.user, datetime__date=today,status__in=['failed']).order_by('-datetime')
    tradebook = Order.objects.filter(user=request.user)
    wallet = ((request.user.margin/100)*request.user.wallet)
    settings = charges.objects.first()
    tax = settings.tax
    charge = settings.intraday_buy_charge

    # ---------------CONTEXT-----------
    context = {
        "tradebook":tradebook,
        "completed":completed,
        "pending":pending,
        "initiated":initiated,
        "failed":failed,
        "wallet":wallet,
        "tax":tax,
        "charges":charge,
    }
    return render(request,'orders.html',context)

@login_required
def portfolio(request):
    portfolio_symbollist = []
    today = timezone.now().date()
    holdings = Position.objects.filter(user=request.user,is_holding=True,is_closed=False).exclude(created_at__date=today)
    for x in holdings:
        portfolio_symbollist.append(x.instrument_key)
    positions = Position.objects.filter(user=request.user,created_at__date=today)
    for x in positions:
        portfolio_symbollist.append(x.instrument_key)
    ppnl = 0
    for i in positions:
        ppnl = ppnl + i.realised_pnl
    hpnl = 0.0
    for x in holdings:
        hpnl = hpnl + x.realised_pnl
    wallet = request.user.wallet
    margin = request.user.margin
    settings = charges.objects.first()
    charge = settings.intraday_buy_charge
    tax = settings.tax
    option_chain = {}
    lotob = Option_Lot_Size.objects.all()
    for x in lotob:
        option_chain[x.symbol] = x.quantity
    # ---------------CONTEXT-----------
    context = {
        "positions":positions,
        "holdings":holdings,
        "ppnl":round(ppnl,2),
        "hpnl":round(hpnl,2),
        "portfolio_symbollist":portfolio_symbollist,
        'wallet':wallet,
        'margin':margin,
        'charges':charge,
        'tax':tax,
        'option_chain':json.dumps(option_chain),
    }
    return render(request,'portfolio.html',context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = BankInfoForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'KYC completed !')
        else:
            messages.error(request, 'Invalid Details')
    return render(request,'profile.html')

# WATCHLIST
@login_required
def add_to_watchlist(request):
    if request.method == 'POST':
        form = WatchlistForm(request.POST)
        if form.is_valid():
            watchlist = form.save(commit=False)
            watchlist.user = request.user
            watchlist.save()
            return JsonResponse({'success': True, 'message': 'Added to watchlist successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'Form data is invalid.'})
    else:
        form = WatchlistForm()
    return render(request, 'market.html', {'form': form})


# TRANSACTIONS
@login_required
def async_transact(request):
    from app.symbols.instruments import get_exchange
    if request.method == 'POST':
        instrument_key = request.POST.get("instrument")
        token = request.POST.get("token")
        symbol = request.POST.get("symbol")
        price = float(request.POST.get("price"))
        quantity = int(request.POST.get("quantity"))
        order_type = request.POST.get("order_type")
        product = request.POST.get("product")
        type = request.POST.get("type")
        stoploss = request.POST.get("stoploss")
        target = request.POST.get("target")
        segment = get_exchange(token)
        if not market_open(segment):
            return JsonResponse({'success': False, 'message': 'Market Closed !'})
        if segment == 'NSE_FO' or segment == 'BFO_FO' or segment == 'MCX_FO':
            tempsymbol = get_symbol(symbol)
            ob = Option_Lot_Size.objects.filter(symbol=tempsymbol).first()
            if ob is not None:
               quantity = quantity * ob.quantity
        status = "failed"
        if type == 'MARKET':
            status = market_order(request.user,symbol,instrument_key,token,quantity,order_type,product,stoploss,target)
        else:
            status = initiate_limit_order(request.user,symbol,instrument_key,token,price, quantity,order_type,product,stoploss,target)
        if status == "failed":
            return JsonResponse({'success': False, 'message': 'Order executed but failed !'})
        else:
            # messages.success(request,'Order placed successfully.')
            return JsonResponse({'success': True, 'message': 'Order Placed successfully'})
    else:
        return redirect('/orders')


def cancel_order(request, order_id):
    try:
        cancelob = Order.objects.filter(user=request.user).get(order_id=order_id)
        cancelob.status = 'cancelled'
        return JsonResponse({'success': True, 'message': 'Order Cancelled successfully'})
    except:
        return JsonResponse({'success': False, 'message': 'Order Cancellation Failed'})

@login_required
def cancelorder(request, order_id):
    try:
        cancelob = Order.objects.filter(user=request.user).get(order_id=order_id)
        cancelob.status = 'cancelled'
        cancelob.save()
        messages.error(request,'Order Cancelled Successfully')
        return redirect('/orders')
    except:
        messages.error(request,'Order Cancellation Failed')
        return redirect('/orders')

@login_required
def place_order(request):
    if request.method == 'POST':
        form = (request.POST)
        if form.is_valid():
            create_order = form.save(commit=False)
            create_order.user = request.user
            create_order.save()
            return JsonResponse({'success': True, 'message': 'Added to watchlist successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'Form data is invalid.'})
    else:
        return JsonResponse({'status' : 'Invalid Request'})

@login_required
def trade_charges(request):
    odr = Order.objects.filter(user=request.user,status='completed')
    tcharge = 0
    for i in odr:
        tcharge = tcharge + i.charges
    context = {
        'odr':odr,
        'tcharge':round(tcharge,2)
    }
    return render(request,'trade_charges.html',context)


@login_required
def pnl(request):
    odr = Position.objects.filter(user=request.user)
    tpnl = 0
    for i in odr:
        tpnl = tpnl + i.realised_pnl
    odr = Position.objects.filter(user=request.user,quantity=0)
    context = {
        'odr':odr,
        'tpnl':round(tpnl,2)
    }
    return render(request,'pnl.html',context)

@login_required
def transactions(request):
    if request.method == 'POST':
        amount = request.POST.get("amount")
        ob = Transaction.objects.filter(user=request.user,status='REQUESTED')
        check_amount = int(amount)
        for x in ob:
            check_amount = check_amount + x.amount
        if int(check_amount) <= request.user.wallet:
            Transaction.objects.create(user=request.user,amount=int(amount))
            messages.success(request,'Request added, your amount will be transferred to your account within 24 hours.')
        else:
            messages.error(request,'Invalid amount ! Please enter correct amount and try again.')
    trans = Transaction.objects.filter(user=request.user)
    context = {
        'trans':trans
    }
    return render(request,'transactions.html',context)



from django.shortcuts import render,HttpResponse
from settings.models import Upstox
import requests


def upstox_cred(request,secret):
    if request.method == 'GET':
        try:
            print(secret)
            code = request.GET.get('code')
            obj = Upstox.objects.filter(secret_key=secret).first()
            obj.code = code
            obj.save()
            data = {
                'code': code,
                'client_id': obj.api_key,
                'client_secret': obj.secret_key,
                'redirect_uri': obj.redirect_uri,
                'grant_type': 'authorization_code',
            }
            url = 'https://api-v2.upstox.com/login/authorization/token'
            response = requests.post(url,data=data)
            response = response.json()
            obj.access_token = response['access_token']
            obj.save()
            UpstoxAccessTokens.objects.create(access_token=obj.access_token)
            return redirect('/admin/settings/upstox')
        except Exception as e:
            messages.error(request,f'Something went wrong ! {e}')
            return redirect('/admin/settings/upstox')
        
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upstox_access_tokens(request):
    if request.method == 'POST':
        ob = UpstoxAccessTokens.objects.all()
        tokens = [x.access_token for x in ob]
        return JsonResponse({'tokens':tokens})


def limit_orders(request):
    from data.orders import task
    thread = Thread(target=task)
    thread.start()
    return HttpResponse('<h1>LIMIT ORDER STARTED</h1>')
