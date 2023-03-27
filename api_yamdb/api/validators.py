from django.core.validators import RegexValidator

user_regex_validator = RegexValidator(
    regex=r'^[\w.@+-]+$',
    message='Имя пользователя содержит недопустимый символ')
