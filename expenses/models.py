from django.db import models
from django.db.models import F,Q
from datetime import date
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class Expense(models.Model):
    amount = models.FloatField(blank=False)
    date = models.DateField(default=now)
    description = models.TextField(blank=True, null=False)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255, blank=False)
    
    def __str__(self):
        return self.category
    
    class Meta:
        ordering: ["-date"]
        constraints = [
			models.CheckConstraint(
       			condition=models.Q(date__gte = date(1900, 1, 1)),
                name='date_cannot_be_before_1900'),
			models.CheckConstraint(
       			condition=models.Q(date__lte = date(2200, 1, 1)),
                name='date_cannot_be_after_2200'),
		] 
	# __gte: Greater than or Equal. 
    
    
class Category(models.Model):
	name=models.CharField(max_length=255)
 
	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "categories"