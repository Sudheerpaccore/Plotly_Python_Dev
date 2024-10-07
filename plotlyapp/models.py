from django.db import models

# Create your models here.
class SalesData(models.Model):
    product = models.CharField(max_length=100)
    sales = models.IntegerField()
    month = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.product} - {self.sales}"
