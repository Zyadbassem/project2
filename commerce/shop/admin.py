from django.contrib import admin
from shop.models import Item
from shop.models import User
from shop.models import Bid


class ItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(Item, ItemAdmin)

class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)

class BidAdmin(admin.ModelAdmin):
    pass

admin.site.register(Bid, BidAdmin)
# Register your models here.
