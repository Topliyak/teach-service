from django.db import models
from django.contrib.auth.models import User


class Section(models.Model):
	name = models.CharField(
		max_length=200,
		blank=False
	)

	order = models.PositiveIntegerField(
		blank=False,
	)

	parent = models.ForeignKey(
		to='self',
		on_delete=models.CASCADE,
		null=True,
	)


class Page(models.Model):
	name = models.CharField(
		max_length=200,
		blank=True,
	)

	order = models.PositiveIntegerField(
		blank=False,
	)

	section = models.ForeignKey(
		to=Section,
		on_delete=models.CASCADE,
		null=False,
	)


class Course(models.Model):
	name = models.CharField(
		max_length=200,
		blank=False,
	)

	main_section = models.OneToOneField(
		to=Section,
		on_delete=models.CASCADE,
	)

	author = models.ForeignKey(
		to=User,
		on_delete=models.CASCADE,
		null=False,
	)
