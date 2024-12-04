from django.db import models
from django.db.models import Sum
from decimal import Decimal

class UserSubscriptionManager(models.Manager):
    def unpaid(self):
        return self.filter(is_paid=False)
    
    def paid(self):
        return self.filter(is_paid=True)
    
    def total_unpaid_amount(self) -> Decimal:
        return self.unpaid().aggregate(total=Sum('amount'))['total'] or Decimal('0')
    
    def mark_as_paid(self, subscription_id: int):
        return self.filter(id=subscription_id).update(is_paid=True)
