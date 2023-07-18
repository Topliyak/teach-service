from pathlib import Path
import json
from typing import Dict, Any


def get(attr):
	return _variables[attr]


BASE_DIR = Path(__file__).resolve().parent.parent

_variables: Dict[str, Any]

with open(BASE_DIR / 'env.json') as conf_file:
	_variables = json.loads(conf_file.read())
