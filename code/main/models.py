from django.db import models
from django.utils import timezone


# Create your models here.
class Employee(models.Model):
    employee_name = models.CharField(max_length=255, null=True)
    employee_email = models.CharField(max_length=255, null=True)
    employee_phone = models.IntegerField(null=True)
    employee_password = models.CharField(max_length=255, null=True)
    employee_address = models.CharField(max_length=255, null=True)
    image = models.FileField(null=True)
    employee_latitude = models.CharField(max_length=255, null=True)
    employee_longitude = models.CharField(max_length=255, null=True)
    employee_gender = models.BooleanField(default=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, null=True)

    class Meta:
        db_table="employees"

# ///////////////////
# For CheckIn
# //////////////////
class CheckIn(models.Model):
    name = models.CharField(max_length=255, null=True)
    day = models.CharField(max_length=255, null=True)
    time = models.CharField(max_length=50, null=True)
    user_id = models.IntegerField(null=True)
    # user_id = models.ForeignKey(Employee, on_delete=models.CASCADE ,null=True)
    created_at = models.DateTimeField(default=timezone.now, null=True)

    class Meta:
        db_table="checkin"

# ///////////////////
# For CheckOut
# //////////////////
class CheckOut(models.Model):
    name = models.CharField(max_length=255, null=True)
    day = models.CharField(max_length=255, null=True)
    time = models.CharField(max_length=50, null=True)
    user_id = models.IntegerField(null=True)
    created_at = models.DateTimeField(default=timezone.now, null=True)

    class Meta:
        db_table="checkout"


# ///////////////////
# For Request a Demo
# //////////////////
class RequestDemo(models.Model):
    name = models.CharField(max_length=255, null=True)
    company_name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    phone = models.IntegerField(null=True)
    created_at = models.DateTimeField(default=timezone.now, null=True)

    class Meta:
        db_table="request_demo"


# ///////////////////
# For Contact us
# //////////////////
class ContactUs(models.Model):
    name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    message = models.CharField(max_length=1000, null=True)
    created_at = models.DateTimeField(default=timezone.now, null=True)

    class Meta:
        db_table = "contact_us"





