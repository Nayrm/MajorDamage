from django.contrib.auth.models import User
from django.db import models


class SavedRepair(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    sku = models.IntegerField()
    lp = models.CharField(max_length=255)
    repair = models.TextField()

    def __str__(self):
        return f"{self.date} {self.time} - {self.user.first_name} {self.user.last_name} - SKU: {self.sku}, LP: {self.lp}"  


