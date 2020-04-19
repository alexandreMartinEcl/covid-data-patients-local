import django.db.models.fields as fields


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

    if getattr(field, 'choices', []) and not isinstance(field, (fields.NullBooleanField, fields.BooleanField)):
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

