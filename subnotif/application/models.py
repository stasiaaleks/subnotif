from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Subscription(models.Model):
    service_name = models.CharField(max_length=256)
    payment_day = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_link = models.URLField(blank=True, null=True)
    is_paid = models.BooleanField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.service_name}: {self.amount} on each day {self.payment_day}"

