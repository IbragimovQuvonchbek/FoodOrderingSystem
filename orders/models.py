from django.db import models
from django.contrib.auth.models import User

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return self.name

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Submitted', 'Submitted'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    customer_email = models.EmailField(blank=True, null=True)
    delivery_address = models.TextField(blank=True, null=True)
    delivery_lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    delivery_lng = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.menu_item.price * item.quantity for item in self.orderitem_set.all())

    def __str__(self):
        return f"#{self.id}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"
