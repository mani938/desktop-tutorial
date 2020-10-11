from django.db import models

class ProductModel(models.Model):
    pno=models.AutoField(primary_key=True)
    name=models.CharField(unique=True,max_length=100)
    price=models.FloatField()
    quantity=models.IntegerField()