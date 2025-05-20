from flask import Blueprint, request, redirect, render_template, flash, current_app, url_for
from . import mysql
from .utils import generate_short_code
from .db import insert_url, get_long_url, is_short_code_exists

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_code = generate_short_code()

        while is_short_code_exists(short_code):
            short_code = generate_short_code()

        insert_url(long_url, short_code)
        short_url = request.host_url + short_code
        flash(f'Short URL: {short_url}')
        return redirect(url_for('main.index'))

    return render_template('index.html')

@main.route('/<short_code>')
def redirect_to_long_url(short_code):
    result = get_long_url(short_code)
    if result:
        return redirect(result[0])
    else:
        return 'URL not found', 404