import re
from urllib.parse import urljoin
from http import HTTPStatus

from flask import jsonify, request

from . import app
from .constants import REGULAR_EXPRESSION_FOR_CUSTOM_ID, MAX_LINK_LENGTH
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id, form_and_add_url_to_db


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса', HTTPStatus.BAD_REQUEST)
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!', HTTPStatus.BAD_REQUEST)
    base_url = request.base_url.split('/api/')[0]
    if 'custom_id' in data:
        custom_id = data['custom_id']
        if custom_id is None or custom_id == '':
            custom_id = get_unique_short_id()
        elif (
                not re.fullmatch(
                    REGULAR_EXPRESSION_FOR_CUSTOM_ID, custom_id
                ) or len(data['custom_id']) > MAX_LINK_LENGTH
        ):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки',
                HTTPStatus.BAD_REQUEST
            )
    else:
        custom_id = get_unique_short_id()
    if URLMap.query.filter_by(short=custom_id).first():
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.',
            HTTPStatus.BAD_REQUEST
        )
    url = form_and_add_url_to_db(data['url'], custom_id)
    return jsonify(
        {
            'url': url.original,
            'short_link': urljoin(base_url, url.short)
        }
    ), HTTPStatus.CREATED


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_short_url(short: str):
    url_model = URLMap.query.filter_by(short=short).first()
    if url_model is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify(
        {
            'url': url_model.original
        }
    ), HTTPStatus.OK
