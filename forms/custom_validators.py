from wtforms import ValidationError


class EndsWith(object):
    def __init__(self, end_char, message=None):
        self.end_char = end_char
        if not message:
            message = f'Строка не должна заканчиваться на "{end_char}"'
        self.message = message

    def __call__(self, form, field):
        l = field.data or ""
        if l.endswith(self.end_char):
            raise ValidationError(self.message)
