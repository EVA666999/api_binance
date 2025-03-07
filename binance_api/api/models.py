from django.db import models

class TradeData(models.Model):
    pair = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=18, decimal_places=8)

    def __str__(self):
        return f'{self.pair} - {self.price}'
