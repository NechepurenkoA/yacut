from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Regexp, Optional, length

from .constants import REGULAR_EXPRESSION_FOR_CUSTOM_ID
from .models import URLMap


class URLForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка', validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Regexp(REGULAR_EXPRESSION_FOR_CUSTOM_ID),
            Optional(),
            length(1, 16)
        ]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(form, field):
        if URLMap.query.filter_by(short=field.data).first():
            raise ValidationError('Предложенный вариант короткой ссылки уже существует.')
