from django.db import models
from .base import BaseAnswer


class FewVariantsAnswer(BaseAnswer):
	multy_correct = models.BooleanField()


class AnswerVariant(models.Model):
	fvansw = models.ForeignKey(
		to=FewVariantsAnswer,
		on_delete=models.CASCADE,
		null=False,
	)

	inner_id = models.SmallIntegerField()
	correct = models.BooleanField()
	title = models.TextField()
