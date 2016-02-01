## custom validators
from __future__ import unicode_literals

import jsonschema
from rest_framework.exceptions import ParseError

from push_endpoint import schemas


class JsonSchema(object):
    def __call__(self, value):
        try:
            format_checker = jsonschema.FormatChecker()
            jsonschema.validate(value.get('jsonData', {}), schemas.share, format_checker=format_checker)
        except jsonschema.exceptions.ValidationError as error:
            raise ParseError(detail=error.message)
