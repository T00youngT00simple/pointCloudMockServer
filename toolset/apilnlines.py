
from rest_framework.exceptions import ValidationError
from datetime import datetime, timedelta

def extractApiKwargs(valueDict, keys, convertNames=None):
    if not convertNames:
        convertNames = {}

    kwargs = {}
    for key in keys:
        if key in valueDict:
            value = valueDict[key]
            if isinstance(value, str):
                value.strip()

            kwargs[convertNames.get(key) or key] = value

    return kwargs
