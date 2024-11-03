from django.db import models

class Event(models.Model):
    event_name = models.CharField(max_length=255)
    event_date = models.DateField()
    event_time = models.TimeField()
    place = models.CharField(max_length=255)
    category_type = models.CharField(max_length=100, blank=True, null=True)
    priority = models.CharField(
        max_length=10,
        choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')],
        default='Medium'
    )

    def __str__(self):
        return self.event_name
