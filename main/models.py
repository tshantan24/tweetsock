from django.db import models

# Create your models here.
class Handle(models.Model):
    handle = models.CharField(max_length=100)
    party = models.IntegerField()

    def __str__(self):
    	return self.handle