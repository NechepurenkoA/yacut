from urllib.parse import urljoin

from flask import abort, render_template, flash, request, redirect

from . import app
from .forms import URLForm
from .models import URLMap
from .utils import get_unique_short_id, form_and_add_url_to_db


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        custom_id = (get_unique_short_id() if form.custom_id.data is None or form.custom_id.data == ''
                     else form.custom_id.data)
        url_model = form_and_add_url_to_db(form.original_link.data, custom_id)
        flash(urljoin(request.base_url, url_model.short), category='link')
        return render_template('create_short_url.html', form=form)
    return render_template('create_short_url.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_url(short: str):
    url = URLMap.query.filter_by(short=short).first()
    if url is None:
        abort(404)
    return redirect(url.original)
