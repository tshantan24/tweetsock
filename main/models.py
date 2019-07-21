from django.db import models

# Create your models here.
class handles(models.Model):
    handle = models.CharField(max_length=100)
    party = models.FloatField()

    def __str__(self):
    	return self.party