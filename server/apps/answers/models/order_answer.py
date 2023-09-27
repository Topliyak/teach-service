from django.db import models
from .base import BaseAnswer


class OrderAnswer(BaseAnswer):
	pass


class OrderAnswerElement(models.Model):
	title = models.TextField()
	correct_order = models.IntegerField()

	order_answ = models.ForeignKey(
		to=OrderAnswer,
		on_delete=models.CASCADE,
		null=False,
	)
