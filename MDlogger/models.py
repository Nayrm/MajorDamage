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
    
class Projects(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    assignedto = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_projects')
    due = models.DateField()
    department = models.CharField(max_length=80)
    project = models.CharField(max_length=200)
    description = models.TextField()
    STATUS_CHOICES = [
        ('Incomplete', 'Incomplete'),
        ('Completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Incomplete')

    def __str__(self):
        return f"{self.date} {self.time} - {self.user.first_name} {self.user.last_name} - {self.project} - {self.description} - {self.status}"