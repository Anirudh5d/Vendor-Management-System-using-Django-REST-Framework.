from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Avg, F

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def clean(self):
        if Vendor.objects.filter(vendor_code=self.vendor_code).exclude(pk=self.pk).exists():
            raise ValidationError({'vendor_code': 'Vendor code must be unique'})

    def calculate_on_time_delivery_rate(self):
        completed_purchases = self.purchaseorder_set.filter(status='completed')
        total_completed_purchases = completed_purchases.count()
        if total_completed_purchases > 0:
            on_time_deliveries = completed_purchases.filter(delivery_date__lte=F('delivery_date')).count()
            self.on_time_delivery_rate = (on_time_deliveries / total_completed_purchases) * 100
            self.save()

    def calculate_quality_rating_avg(self):
        completed_purchases = self.purchaseorder_set.filter(status='completed').exclude(quality_rating=None)
        total_completed_purchases = completed_purchases.count()
        if total_completed_purchases > 0:
            avg_rating = completed_purchases.aggregate(avg_rating=Avg('quality_rating'))['avg_rating']
            self.quality_rating_avg = avg_rating
            self.save()

    def calculate_average_response_time(self):
        acknowledged_purchases = self.purchaseorder_set.filter(acknowledgment_date__isnull=False)
        total_acknowledged_purchases = acknowledged_purchases.count()
        if total_acknowledged_purchases > 0:
            avg_response_time = acknowledged_purchases.aggregate(avg_response_time=Avg(F('acknowledgment_date') - F('issue_date')))['avg_response_time']
            self.average_response_time = avg_response_time
            self.save()

    def calculate_fulfillment_rate(self):
        completed_purchases = self.purchaseorder_set.filter(status='completed')
        total_completed_purchases = completed_purchases.count()
        if total_completed_purchases > 0:
            successful_purchases = completed_purchases.exclude(issue_date__gte=F('acknowledgment_date')).count()
            fulfillment_rate = (successful_purchases / total_completed_purchases) * 100
            self.fulfillment_rate = fulfillment_rate
            self.save()

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if self.delivery_date and self.order_date and self.delivery_date <= self.order_date:
            raise ValidationError({'delivery_date': 'Delivery date must be after the order date'})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == 'completed':
            self.vendor.calculate_on_time_delivery_rate()
            self.vendor.calculate_quality_rating_avg()
            self.vendor.calculate_average_response_time()
            self.vendor.calculate_fulfillment_rate()

    def __str__(self):
        return self.po_number

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor} - {self.date}"
