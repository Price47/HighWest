from django.db import models

class Customer(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    street_address = models.CharField(max_length=128)
    state = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=128)

class Transaction(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    purchase_status = models.CharField(max_length=16)
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=1024)
    purchase_amount = models.FloatField()
    transaction_date = models.DateTimeField()
