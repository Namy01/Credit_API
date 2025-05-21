from django.contrib import admin
from .models import Buyer_credit, Item_purchased, Item

admin.site.register(Buyer_credit)
admin.site.register(Item_purchased)
admin.site.register(Item)
