from django.contrib import admin
from .models import Subscription

@admin.register(Subscription)
class ChatConfigAdmin(admin.ModelAdmin):
    list_display = ("service_name", "amount", "payment_day")
    search_fields = ("service_name",)

