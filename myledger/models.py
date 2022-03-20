from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class MyGroup(models.Model):
    members = models.ManyToManyField(User, through='Tally')
    groupName = models.CharField(max_length=100, null=True)
    def __str__(self):
        return str(self.groupName)

class Tally(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(MyGroup, on_delete=models.CASCADE, default='')
    balance = models.IntegerField(null=True,default=0)

    class Meta:
        unique_together = [['user','group']]

class Transaction(models.Model):
    group = models.ForeignKey(MyGroup, on_delete=models.CASCADE, default='')
    lender = models.ForeignKey(User,on_delete=models.PROTECT, related_name='lender')
    borrower = models.ForeignKey(User,on_delete=models.PROTECT, related_name='borrower')
    amount = models.PositiveIntegerField()
    lable = models.TextField(max_length=100,null=True)
    transactionDate = models.DateTimeField(auto_now=True)