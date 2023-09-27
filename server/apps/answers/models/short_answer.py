from django.db import models
from .base import BaseAnswer


class ShortAnswer(BaseAnswer):
	only_digits = models.BooleanField()
	ignore_case = models.BooleanField()
	ignore_spaces = models.BooleanField()
	ignore_border_spaces = models.BooleanField()
