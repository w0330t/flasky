from datetime import datetime

from flask import session, render_template, redirect, url_for, current_app

from ..email import send_email
from . import main
from ..models import User
from .forms import NameForm
from .. import db

@main.route('/', methods = ['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            session['known'] = False
            # 如果有新用户则发送一封邮件
            if current_app.config['FLASKY_ADMIN']:
                send_email(current_app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user = user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form = form,
                           name = session.get('name'),
                           konwn = session.get('known', False),
                           current_time = datetime.utcnow())