from django.contrib import admin

from .models import Auction, Watchlist, User, Comments, Bids
# Register your models here.

admin.site.register(User)
admin.site.register(Auction)
admin.site.register(Watchlist)
admin.site.register(Comments)
admin.site.register(Bids)