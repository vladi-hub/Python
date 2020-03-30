from __future__ import unicode_literals
from django.db import models
from django.conf import settings

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Location(models.Model):
	user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
		)
	name = models.CharField(max_length=50)
	address = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)
	LOCATION_TYPE =	(
        ('st', 'Storage'),
        ('fl', 'Flat'),
        ('gr', 'Garage'),
        ('ho', 'House'),
		('ba', 'Bank'),
		('oth', 'Other'),
    )
	locationType = models.CharField(
        max_length=2,
        choices=LOCATION_TYPE,
        default='ho',
    )
	def __str__(self):
		return self.name

	
	
class Asset(models.Model):
	location = models.ForeignKey(Location, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	assettype = models.CharField(max_length=50)
	serial = models.CharField(max_length=200)
	purchasedate = models.DateTimeField('purchased date')
	price = models.FloatField(default=0)
	document = models.FileField(upload_to='uploads/')
	
	REQUIRED_FIELDS = ['name', 'assettype', 'serial']
	
	def __str__(self):
		return self.name
	
class Service(models.Model):
	location = models.ForeignKey(Location, on_delete=models.CASCADE)
	servicename = models.CharField(max_length=200)
	provider = models.CharField(max_length=200);
	clientno = models.CharField(max_length=200)
	purchasedate = models.DateTimeField('purchased date')
	document = models.FileField(upload_to='uploads/')
	def __str__(self):
		return self.servicename