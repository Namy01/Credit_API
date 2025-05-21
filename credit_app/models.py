from django.db import models

from django.db import models
from django.conf import settings

class Buyer_credit(models.Model):
   
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='credit',
    )
    credit_amount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.buyer.username} - Credit: {self.credit_amount}"


class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()  

    def __str__(self):
        return self.name


class Item_purchased(models.Model):
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='purchases',
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.SET_NULL,  
        null=True,
        blank=True,
    )
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        item_name = self.item.name if self.item else "Unknown Item"
        item_price = self.item.price if self.item else "Unknown Price"
        return f"{item_name} purchased by {self.buyer.username} Total cost is {item_price} on {self.purchase_date:%Y-%m-%d}"


