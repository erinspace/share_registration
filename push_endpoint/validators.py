## custom validators
from __future__ import unicode_literals

import json
import jsonschema
from rest_framework.exceptions import ParseError, ValidationError

from push_endpoint import schemas


class JsonSchema(object):
    def __call__(self, value):
        json_text = value.get('jsonData')
        # TODO - figure out why this isn't a dict automatically - this is
        # problematic with pushed data with single quotes in it!!
        json_text = json_text.replace("u'", '"').replace("'", '"')
        try:
            json_data = json.loads(json_text)
        except ValueError as e:
            raise ValidationError(
                'Error: {} Please make sure your jsonData field is valid JSON.'.format(e)
            )

        try:
            jsonschema.validate(json_data, schemas.share)
        except jsonschema.exceptions.ValidationError as error:
            raise ParseError(detail=error.message)
