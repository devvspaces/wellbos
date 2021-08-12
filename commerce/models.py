import uuid

from django.db import models


class Bag(models.Model):
    product = models.ForeignKey('product.Product', on_delete = models.CASCADE)
    quantity = models.IntegerField(default=1)
    guest = models.ForeignKey('account.GuestUser', on_delete = models.DO_NOTHING)
    user = models.ForeignKey('account.User', on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return str(self.uid)


class Order(models.Model):
    STATUS = (
        ('1', 'Pending',),
        ('2', 'In dispatch',),
        ('3', 'Delivered',),
        ('4', 'Waiting for rating',),
        ('5', 'Completed',),
    )
    bag = models.ForeignKey(Bag, on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(choices=STATUS, max_length=5)

    def __str__(self):
        return str(self.uid)