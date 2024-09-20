from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .constants import VALID_SHORT_ID
from .views import get_unique_short_id

@app.route('/api/id/<string:short_link>/', methods=['GET'])
def get_link(short_link):
    original_link = URLMap.query.filter_by(short=short_link).first()
    if original_link is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify(dict(url = original_link.original)), 200


@app.route('/api/id/', methods=['POST'])
def add_link():
    if not request.is_json:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    data = request.get_json()
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
    return jsonify({'url': link.original, 'short_link': short_link}), 201
