from django.db import models


class Wallet(models.Model):

    class Meta:
        db_table = "Wallet"

    user_id = models.IntegerField(default=0)
    address = models.CharField(max_length=42)
    private_key = models.CharField(max_length=64)
    public_key = models.CharField(max_length=64)
