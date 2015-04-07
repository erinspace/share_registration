## custom validators
import jsonschema
from rest_framework.exceptions import ParseError

from push_endpoint import schemas


class JsonSchema(object):
    def __call__(self, value):

        json = value.get('jsonData')
        try:
            jsonschema.validate(json, schemas.share)
        except ValueError as error:
            raise ParseError(detail=error.message)
