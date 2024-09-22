from flask import jsonify, request
from http import HTTPStatus

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .constants import VALID_SHORT_ID
from .views import get_unique_short_id


@app.route('/api/id/<string:short_link>/', methods=['GET'])
def get_link(short_link):
    original_link = URLMap.query.filter_by(short=short_link).first()
    if original_link is None:
        raise InvalidAPIUsage(
            'Указанный id не найден', HTTPStatus.NOT_FOUND.value
        )
    return jsonify(dict(url=original_link.original)), HTTPStatus.OK.value


@app.route('/api/id/', methods=['POST'])
def add_link():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if 'custom_id' not in data or not data['custom_id']:
        data['custom_id'] = get_unique_short_id()
    if not VALID_SHORT_ID.match(data['custom_id']):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    link = URLMap()
    link.from_dict(data)
    db.session.add(link)
    db.session.commit()
    short_link = f'{request.host_url}{link.short}'
    return jsonify(
        {'url': link.original, 'short_link': short_link}
    ), HTTPStatus.CREATED.value
