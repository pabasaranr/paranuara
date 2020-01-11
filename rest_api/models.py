from django.db import models
from django_mysql.models import ListTextField
from .config import VEGETABLES, FRUITS


class CreatedUpdatedModel(models.Model):

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class Company(CreatedUpdatedModel):
	index = models.PositiveIntegerField(unique=True)
	company = models.CharField(max_length=128, unique=True)

	def __str__(self):
		return self.index


class Citizen(CreatedUpdatedModel):
	index = models.PositiveIntegerField(unique=True)
	guid = models.CharField(max_length=48)
	name = models.CharField(unique=True, max_length=128)
	gender = models.CharField(max_length=6)
	age = models.PositiveIntegerField()
	has_died = models.NullBooleanField()
	eyeColor = models.CharField(max_length=20)
	company_id = models.IntegerField()
	email = models.EmailField(max_length=256)
	phone = models.CharField(max_length=17)
	address = models.TextField()
	balance = models.CharField(max_length=64)
	about = models.TextField()
	favouriteFood = ListTextField(base_field=models.CharField(max_length=20))
	registered = models.CharField(max_length=30)
	picture = models.URLField(max_length=256)
	friends = ListTextField(base_field=models.PositiveIntegerField())
	greeting = models.TextField()
	tags = ListTextField(base_field=models.CharField(max_length=20))
	fruits = ListTextField(base_field=models.CharField(max_length=20))
	vegetables = ListTextField(base_field=models.CharField(max_length=20))

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.fruits = list(set(self.favouriteFood) & FRUITS)
		self.vegetables = list(set(self.favouriteFood) & VEGETABLES)
		super(Citizen, self).save(*args, **kwargs)
