from django.contrib import admin
from django.http import HttpRequest
from .models import Subscription, Company
from django.db.models import QuerySet

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("company", "subscriber", "amount", "payment_day", "is_paid")
    search_fields = ("company",)
    
    actions = ["mark_as_paid", "mark_as_unpaid"]
    
    @admin.action(description="Mark selected subscriptions as paid")
    def mark_as_paid(self, request: HttpRequest, queryset: QuerySet):
        updated = queryset.update(is_paid=True)
        self.message_user(
            request,
            f"Successfully marked {updated} subscription(s) as paid."
        )
    
    @admin.action(description="Mark selected subscriptions as unpaid")
    def mark_as_unpaid(self, request: HttpRequest, queryset: QuerySet):
        updated = queryset.update(is_paid=False)
        self.message_user(
            request,
            f"Successfully marked {updated} subscription(s) as unpaid."
        )

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
