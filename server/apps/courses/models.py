from django.db import models
from django.contrib.auth.models import User
from server.apps.answers.models import Answer


class AccessLimiterType(models.Model):
	name = models.CharField(
		max_length=100,
	)


class Course(models.Model):
	name = models.CharField(
		max_length=200,
		blank=False,
	)

	author = models.ForeignKey(
		to=User,
		on_delete=models.CASCADE,
		null=False,
	)

	access_limiter = models.ForeignKey(
		to=AccessLimiterType,
		on_delete=models.CASCADE,
		null=True,
		blank=True,
	)


class Section(models.Model):
	order = models.SmallIntegerField()

	course = models.ForeignKey(
		to=Course,
		on_delete=models.CASCADE,
		null=False,
	)

	parent = models.ForeignKey(
		to='self',
		on_delete=models.CASCADE,
		null=True,
		blank=True,
	)

	name = models.CharField(
		max_length=200,
		blank=False,
	)


class Page(models.Model):
	order = models.SmallIntegerField()
	content = models.TextField()

	name = models.CharField(
		max_length=200,
		blank=True,
	)

	section = models.ForeignKey(
		to=Section,
		on_delete=models.CASCADE,
		null=False,
	)

	answer = models.ForeignKey(
		to=Answer,
		on_delete=models.CASCADE,
		null=True,
		blank=True,
	)
