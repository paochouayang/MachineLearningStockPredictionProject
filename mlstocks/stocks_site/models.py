from django.db import models

class Tickers(models.Model):
    ticker = models.CharField(max_length=8)
    description = models.CharField(max_length=300)

