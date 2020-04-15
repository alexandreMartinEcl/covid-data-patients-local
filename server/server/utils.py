"""
Copyright (c) 2020 Magic LEMP

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import string
import random
import django.db.models.fields as fields


def generate_random_string(N: int):
    return ''.join(random.choices(string.ascii_uppercase +
                                  string.digits, k=N))


def get_field_schema(field, title):
    """Returns a JSON Schema representation of a form field."""
    field_schema = {
        'type': 'string',
        'title': title
    }

    # field_schema['title'] = str(field.label)  # force translation

    # if field.help_text:
    #     field_schema['description'] = str(field.help_text)  # force translation

    # if isinstance(field, (fields.URLField, fields.FileField)):
    #     field_schema['format'] = 'uri'
    # elif isinstance(field, fields.EmailField):
    #     field_schema['format'] = 'email'
    if isinstance(field, fields.DateTimeField):
        field_schema['format'] = 'date-time'
    elif isinstance(field, fields.DateField):
        field_schema['format'] = 'date'
    # elif isinstance(field, ProtectedImageField):
    #     field_schema['format'] = 'data-url'
    elif isinstance(field, (fields.DecimalField, fields.FloatField)):
        field_schema['type'] = 'number'
    elif isinstance(field, fields.IntegerField):
        field_schema['type'] = 'integer'
        if getattr(field, 'hidden_boolean', []):
            if field.hidden_boolean:
                field_schema['type'] = 'boolean'
    elif isinstance(field, (fields.NullBooleanField, fields.BooleanField)):
        field_schema['type'] = 'boolean'
        field_schema['default'] = False
    # elif isinstance(field.widget, widgets.CheckboxInput):
    #     field_schema['type'] = 'boolean'

    if getattr(field, 'choices', []) and not isinstance(
            field, (fields.NullBooleanField, fields.BooleanField)):
        field_schema['enum'] = sorted([choice[0] for choice in field.choices])
        # print(field.default)
        # print(type(field.default))
        if type(field.default) is int:
            field_schema['default'] = field.default

    if getattr(field, 'minmax', []):
        field_schema['python_minimum'] = field.minmax[0]
        field_schema['python_maximum'] = field.minmax[1]

    # check for multiple values

    return field_schema
