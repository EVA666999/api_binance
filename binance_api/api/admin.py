from django.contrib import admin
from .models import TradeData

class TradeDataAdmin(admin.ModelAdmin):
    list_display = ('pair', 'price', 'id')
    search_fields = ('pair',)
    list_filter = ('pair',)
admin.site.register(TradeData, TradeDataAdmin)
