from django.db import models
from django.utils import timezone
# Create your models here.
Service_Type_Choices= [
    ('Aadhar Card', "Aadhar Card"),
    ('Pan Card', "Pan Card"),
    ('Voter ID Card', "Voter ID Card"),
    ('Government Services', "Government Services"),
    ('Add Money to Wallet', "Add Money to Wallet"),
    ('Withdrawn Money from Wallet', "Withdraw Money from Wallet"),
    ('Utility Bills', "Utility Bills"),
    ] 

class Customer(models.Model):
    name= models.CharField(("name"), max_length=100)
    service=models.CharField(("service"), max_length=100, choices=Service_Type_Choices)
    phone=models.BigIntegerField(("phone"))
    price=models.BigIntegerField(("price") )
    paid=models.BigIntegerField(("paid"))
    bal=models.BigIntegerField(("bal"))
    date=models.DateTimeField(default=timezone.now)
    status=models.BooleanField(("completed"), default=False)
    cmt=models.CharField(("comments"), max_length=1000)
    
    def __str__(self) -> str:
        return self.name

    @property
    def balupdate(self):
        pr=self.price
        pa=self.paid
        return pr-pa

    def save(self, *args, **kwarg):
        self.bal = self.balupdate
        super(Customer, self).save(*args, **kwarg)
