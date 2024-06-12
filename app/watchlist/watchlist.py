# from app.models import default_watchlist,Watchlist
# from app.symbols.details import symbollist

# def add_to_watchlist(user):
#     dw = default_watchlist.objects.all()
#     for i in dw:
#         try:
#             data = symbollist.get(i.symbol)
#             ob = Watchlist.objects.create(user=user,stock=i.symbol,segment=i.segment,token=data['token'],tag=i.segment)
#         except:
#             pass