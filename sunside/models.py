from django.db import models
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=True, serialize=False, auto_created=True)
    name=models.CharField(max_length=350)
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default=1)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Client(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    address = models.TextField()
    meter_code = models.CharField(max_length=50)
    first_reading = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default=1)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
