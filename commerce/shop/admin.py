from django.contrib import admin
from shop.models import User, Bid, ItemUpdated




class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)

class BidAdmin(admin.ModelAdmin):
    pass

admin.site.register(Bid, BidAdmin)

class ItemUpdatedAdmin(admin.ModelAdmin):
    pass

admin.site.register(ItemUpdated, ItemUpdatedAdmin)

# Register your models here.
