from flask import flash, redirect, render_template, request

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .constants import VALID_SHORT_ID
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if not custom_id:
            custom_id = get_unique_short_id()
        if not VALID_SHORT_ID.match(custom_id):
            flash('Указано недопустимое имя для короткой ссылки')
            return render_template('index.html', form=form)
        if URLMap.query.filter_by(short=custom_id).first() is not None:
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        new_url = URLMap(
            original=form.original_link.data,
            short=custom_id
        )
        db.session.add(new_url)
        db.session.commit()
        flash(
            ('Ваша новая ссылка готова: <a href="' +
             f'{request.base_url}{custom_id}">' +
             f'{request.base_url}{custom_id}</a>')
        )
    return render_template('index.html', form=form)


@app.route('/<string:short_link>')
def redirect_view(short_link):
    original_link = URLMap.query.filter_by(short=short_link).first_or_404()
    return redirect(original_link.original)
