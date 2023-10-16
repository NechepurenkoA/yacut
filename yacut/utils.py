from random import choices

from . import db
from .models import URLMap
from .constants import CHOICES


def get_unique_short_id() -> str:
    """Фун-ция для генерации случайной ссылки."""
    custom_id = "".join(choices(CHOICES, k=6))
    while db.session.query(URLMap.query.filter(URLMap.short == custom_id).exists()).scalar():
        custom_id = "".join(choices(CHOICES, k=6))
    return custom_id


def form_and_add_url_to_db(original_url: str, custom_id: str) -> URLMap:
    """Формирование и добавление модели в базу."""
    url_model = URLMap(
        original=original_url,
        short=custom_id
    )
    db.session.add(url_model)
    db.session.commit()
    return url_model
