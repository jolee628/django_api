from django.db import models


# Create your models here.
# https://docs.djangoproject.com/en/3.1/topics/db/models/
# After writing model definition, run "./manage.py makemigrations" and then "./manage.py migrate"
class FBATransaction(models.Model):
    """
    A single transaction from the FBA transaction report download
    """

    class Meta:
        db_table = "fba_transactions"

    # example_float = models.FloatField(default=0.0)
    # example_date_time = models.DateTimeField(null=False, blank=False)
    # example_foreign_key = models.ForeignKey("django_test.FBATransaction", null=True, blank=True, on_delete=models.SET_NULL)
    # example_char = models.CharField(max_length=32, null=True, blank=True)
    # example_int = models.IntegerField(null=True)
    # example_decimal = models.DecimalField(null=True, max_digits=13, decimal_places=10)
    id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(null=False, blank=False)
    type = models.TextField(max_length=32, null=True, blank=True)
    order_id = models.TextField(max_length=64, null=True, blank=True)
    sku = models.TextField(max_length=32, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    order_state = models.TextField(max_length=32, null=True, blank=True)
    order_city = models.TextField(max_length=32, null=True, blank=True)
    order_postal = models.TextField(max_length=32, null=True, blank=True)
    total_price = models.DecimalField(null=False, blank=False, decimal_places=2, max_digits=13)
