from django.db import models
from .base import BaseAnswer


class MatchAnswer(BaseAnswer):
	pass


class MatchAnswerKey(models.Model):
	inner_id = models.SmallIntegerField()
	title = models.TextField()

	mansw = models.ForeignKey(
		to=MatchAnswer,
		on_delete=models.CASCADE,
		null=False,
	)


class MatchAnswerValue(models.Model):
	inner_id = models.SmallIntegerField()
	key_inid = models.SmallIntegerField()
	title = models.TextField()

	mansw = models.ForeignKey(
		to=MatchAnswer,
		on_delete=models.CASCADE,
		null=False,
	)
