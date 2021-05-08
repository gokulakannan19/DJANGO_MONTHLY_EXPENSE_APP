from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Expense(models.Model):
    MONTH = (
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    amount = models.CharField(max_length=200, null=True, blank=True)
    month = models.CharField(max_length=200, null=True, choices=MONTH)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
