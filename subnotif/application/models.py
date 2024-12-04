from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

from .bot.user.subscriptions_manager import UserSubscriptionManager

class Company(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "companies"
    
    def __str__(self) -> str:
        return f"{self.name}"
    
class Subscription(models.Model):
    subscriber = models.ForeignKey(User, related_name="subscriptions", on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name="subscriptions", on_delete=models.DO_NOTHING)
    payment_day = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_link = models.URLField(blank=True, null=True)
    is_paid = models.BooleanField(blank=True, null=True, default=False)
    
    objects = UserSubscriptionManager()

    def __str__(self) -> str:
        return f"{self.company.name}: {self.amount} € on each day {self.payment_day} of the month"
    
    
class UserWithSubscriptions(User):
    class Meta:
        proxy = True

    @property
    def all_subscriptions(self):
        return self.subscriptions.all() # type: ignore

    @property
    def unpaid_subscriptions(self):
        return self.subscriptions.unpaid() # type: ignore

    @property
    def total_unpaid_amount(self):
        return self.subscriptions.total_unpaid_amount() # type: ignore



