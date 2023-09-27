from django.db import models
from abc import ABC


class AnswerType(models.Model):
	name = models.CharField(
		max_length=100,
	)


class Answer(models.Model):
	answ_type = models.ForeignKey(
		to=AnswerType,
		on_delete=models.CASCADE,
		null=False,
	)

	correct_answer = models.TextField(
		null=True,
	)


class GivenAnswer(models.Model):
	content = models.TextField()

	answer = models.ForeignKey(
		to=Answer,
		on_delete=models.CASCADE,
		null=False,
	)

	file = models.FileField(
		upload_to='%Y/%m/%d',
	)

	created_at = models.DateTimeField(
		auto_now_add=True,
	)


class BaseAnswer(models.Model):
	answer = models.ForeignKey(
		to=Answer,
		on_delete=models.CASCADE,
		null=False,
	)

	class Meta:
		abstract = True
